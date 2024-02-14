
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS

import requests

from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI

import os

load_dotenv('config.env')

openai_api_key = os.getenv('OPENAI_API_KEY')
tmdb_api_token = os.getenv('TMDB_API_TOKEN')

app = Flask(__name__)

CORS(app)

#specific to TMDB 
movie_genre_uniqueCode_List = {
    'Action': 28,
  'Adventure': 12,
    'Mystery': 9648,
  'Romance': 10749,
  'Science Fiction': 878,
  'Thriller': 53,
  'War': 10752,
  'Animation': 16,
  'Comedy': 35,
  'Crime': 80,
  'Documentary': 99,
  'Drama': 18,
  'Family': 10751,
  'Fantasy': 14,
  'History': 36,
  'Horror': 27,
  'Music': 10402,
  'Western': 37
  }

tvshow_genre_uniqueCode_List = {
    'Action & Adventure': 10759,
  'Animation': 16,
  'Comedy': 35,
  'Crime': 80,
  'Documentary': 99,
  'Drama': 18,
  'Family': 10751,
  'Kids': 10762,
  'Mystery': 9648,
  'News': 10763,
  'Reality': 10764,
  'Sci-Fi & Fantasy': 10765,
  'Soap': 10766,
  'Talk': 10767,
  'War & Politics': 10768,
  'Western': 37
  }

ratingQueryList = ['vote_average.gte','vote_average.lte']


@app.route('/process', methods=['POST'])
def process_request():
    if not openai_api_key or not tmdb_api_token:
        return jsonify({"error": "Missing API keys"}), 500
    
    user_query = request.json['query']
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    print(user_query)

    #schema
    schema = {
        "properties": {
            "general_title": {"type": "string"},
            "movie_title": {"type": "string"},
            "tvshow_title" : {"type" : "string"},
            "person_name" : {"type" : "string"},
            "trending_movie": {"type": "string"},
            "trending_tvshow": {"type": "string"},
            "trending_person": {"type": "string"},
            "popular_person": {"type": "string"},
            "genre": {"type": "string"},
            "year" : {"type" : "string"},
            "rating" : {"type" : "string"},
            "movie_or_tvshow" : {"type" : "string"}
        },
    }

    #standarize the json
    def process_data(data):
        standardized_data = {}

        if 'text' in data and data['text']:
            extracted_data = data['text'][0] if isinstance(data['text'], list) else data['text']

            for key in ['general_title', 'movie_title', 'tvshow_title', 'person_name', 'popular_person',
                        'trending_movie','trending_tvshow','trending_person',
                        'year','genre','rating','movie_or_tvshow']:
                
                if key in extracted_data and extracted_data[key]:
                    standardized_data[key] = extracted_data[key]

        return standardized_data
    #LLM code
    llm = ChatOpenAI(openai_api_key = openai_api_key, temperature=0, model="gpt-3.5-turbo")
    chain = create_extraction_chain(schema, llm)

    try:
        data = chain.invoke(user_query)
        standardized_data = process_data(data)

        print(standardized_data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to process the query"}), 500

    def build_search_url(base_url, title, year):
        params = {"query": title, "language": "en-US", "page": 1}
        if year:
            params["year"] = year
        return base_url + "&".join(f"{key}={value}" for key, value in params.items())

    def parse_model_response(content):
        extracted_values = {}
        lines = content.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue
            key, value = line.split(':')
            extracted_values[key.lower().replace(" ", "").strip()] = value.replace("'", "").strip()
        return extracted_values

    def urlBuilder():
        base_url = ""

        base_urls = {
            "general": "https://api.themoviedb.org/3/search/multi?",
            "movie": "https://api.themoviedb.org/3/search/movie?",
            "tvshow": "https://api.themoviedb.org/3/search/tv?",
            "person": "https://api.themoviedb.org/3/search/person?",
            "trending_movie": "https://api.themoviedb.org/3/trending/movie/week?",
            "trending_tvshow": "https://api.themoviedb.org/3/trending/tv/week?",
            "trending_person": "https://api.themoviedb.org/3/trending/person/week?",
            "popular_person": "https://api.themoviedb.org/3/person/popular?",
            "discover_tvshow": "https://api.themoviedb.org/3/discover/tv?language=en-US&page=1&sort_by=popularity.desc",
            "discover_movie": "https://api.themoviedb.org/3/discover/movie?language=en-US&page=1&sort_by=popularity.desc"
        }

        if 'general_title' in standardized_data:
            title = standardized_data['general_title']
            base_url = base_urls['general']
        elif 'movie_title' in standardized_data:
            title = standardized_data['movie_title']
            base_url = base_urls['movie']
        elif 'tvshow_title' in standardized_data:
            title = standardized_data.get('tvshow_title') or standardized_data.get('similar_tvshows')
            base_url = base_urls['tvshow']
        elif 'person_name' in standardized_data:
            title = standardized_data['person_name']
            base_url = base_urls['person']
        elif any(key in standardized_data for key in ['trending_movie', 'trending_tvshow', 'trending_person', 'popular_person']):
            key = next(key for key in ['trending_movie', 'trending_tvshow', 'trending_person', 'popular_person'] if key in standardized_data)
            return base_urls[key] + "language=en-US"
        elif 'movie_or_tvshow' in standardized_data \
            and standardized_data['movie_or_tvshow'].replace(" ", "").replace("-", "").lower().strip() in ["tvshow","tvshows", "tvseries"]:
            base_url = base_urls['discover_tvshow']
        elif 'movie_or_tvshow' in standardized_data \
            and standardized_data['movie_or_tvshow'].replace(" ", "").replace("-", "").lower().strip() in ["movie","movies", "film","films","cinema"]:
            base_url = base_urls['discover_movie']

        if not base_url:
            return ""
        
        # Build search URL for titles
        if base_url in [base_urls['general'], base_urls['movie'], base_urls['tvshow'], base_urls['person']]:
            return build_search_url(base_url, title, standardized_data.get('year'))

        # Handle genre and rating for discover endpoints
        if base_url in [base_urls['discover_tvshow'], base_urls['discover_movie']]:
            prompt = ""
            genre_list = tvshow_genre_uniqueCode_List if base_url == base_urls['discover_tvshow'] else movie_genre_uniqueCode_List
            if 'genre' in standardized_data:
                prompt += f"Match the user's genre description '{standardized_data['genre']}' with the closest genre from this list: {genre_list}"
            if 'rating' in standardized_data:
                prompt += f" Match the user's rating query '{standardized_data['rating']}' with the closest rating query from this list: {ratingQueryList} and rating value"
            if prompt:
                prompt += "Please format your response as follows, if some information is unavailable donot apply: \n\n'Genre: [Your Matched Genre Here]\nRating Query: [Your Matched Rating Query Here]\nRating Value: [Your Matched Rating Value Here]'\n\nEnsure to replace the placeholders with the actual matched genre, rating query, and rating value."
                
                extracted_values = {}
                try:
                    model_response = llm.invoke(prompt)
                    print(model_response.content)
                    extracted_values = parse_model_response(model_response.content)
                except Exception as e:
                    print(e)
        
                print(extracted_values)
                if 'genre' in extracted_values:
                    genre_id = genre_list.get(extracted_values['genre'])
                    base_url += f"&with_genres={genre_id}"
                if 'ratingquery' in extracted_values and extracted_values['ratingquery'] in ratingQueryList:
                    rating_query = extracted_values['ratingquery']
                    base_url += f"&{rating_query}="
                    if 'ratingvalue' in extracted_values and extracted_values['ratingvalue']!='None':
                        base_url += extracted_values['ratingvalue']
                    else:
                        base_url+= '5'
            if 'year' in standardized_data:
                base_url += f"&year={standardized_data['year']}"

        return base_url

    url = urlBuilder()
    print(url)

    def get_data(url):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {tmdb_api_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            return response.text
        except requests.RequestException as e:
            print(e)
            return ""

    info = get_data(url)

    """
    Truncate the input text based on character count to approximate token limit.
    Average token length in GPT-3 is roughly 3 - 4 characters, so for a 4096 token
    limit, we use 12000 characters as a conservative estimate.
    """
    def truncate_to_token_limit(input_text, max_characters=12000):

        if len(input_text) > max_characters:
            return input_text[:max_characters]
        return input_text
    

    info = truncate_to_token_limit(info)
    print(info)

    #generate user response
    def generate_langchain_response(user_query, info):
        prompt = f"""
            Constraint:
            - Only process information and UserQuery related to movies and tvshow.
            UserQuery on Movies and TV Shows: {user_query} 
            Available Information: {info} 
            Response Criteria: 
            - Prioritize information from the 'Available Information' and also use your internal knowledge about movies and TV shows.
            - Exclude Image URL and anyother URLs and  from the response.
            Response:
            """

        try:    
            response = llm.invoke(prompt) 
            return response.content if response else "Error generating response"
        except Exception as e:
            print(e)
            return ""

    langchain_response = generate_langchain_response(user_query, info)
    if langchain_response:
        langchain_response += "\n\n Disclaimer: All the information provided are from TMDB database and ChatGPT3.5."
        final_response = {"data": langchain_response}
        return jsonify({"outputMessage": final_response['data']}), 200
    else:
        return jsonify({"error": "Failed to fetch requested information"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # This should only be used for development.

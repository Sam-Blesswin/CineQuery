
from dotenv import load_dotenv

from flask import Flask, request, jsonify
import requests

from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI

import os

load_dotenv('config.env')

openai_api_key = os.getenv('OPENAI_API_KEY')
tmdb_api_token = os.getenv('TMDB_API_TOKEN')

app = Flask(__name__)

#specific to TMDB 
movie_genreList = {
    'Action': 28,
  'Adventure': 12,
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
  'Mystery': 9648,
  'Romance': 10749,
  'Science Fiction': 878,
  'Thriller': 53,
  'War': 10752,
  'Western': 37
  }

tvshow_genreList = {
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


@app.route('/process', methods=['POST'])
def process_request():
    if not openai_api_key or not tmdb_api_token:
        return jsonify({"error": "Missing API keys"}), 500
    
    user_query = request.json['query']
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

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
            "top_rated_movie": {"type": "string"},
            "top_rated_tvshow": {"type": "string"},
            "popular_person": {"type": "string"},
            "genre": {"type": "string"},
            "year" : {"type" : "string"},
            "movie_or_tvshow": {"type": "string"},
            "rating" : {"type" : "string"},
        },
    }

    #standarize the json
    def process_data(data):
        standardized_data = {}

        if 'text' in data and data['text']:
            extracted_data = data['text'][0] if isinstance(data['text'], list) else data['text']
            print(extracted_data)

            for key in ['general_title', 'movie_title', 'tvshow_title', 'person_name', 
                        'top_rated_movie', 'top_rated_tvshow', 'popular_person',
                        'trending_movie','trending_tvshow','trending_person',
                        'year','movie_or_tvshow','genre','rating']:
                
                if key in extracted_data and extracted_data[key]:
                    standardized_data[key] = extracted_data[key]

        return standardized_data
    #LLM code
    llm = ChatOpenAI(openai_api_key = openai_api_key, temperature=0, model="gpt-3.5-turbo")
    chain = create_extraction_chain(schema, llm)

    try:
        data = chain.invoke(user_query)
        standardized_data = process_data(data)

        if not standardized_data:
            return jsonify({"error": "Requested information not available"}), 400

        print(standardized_data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to process the query"}), 500
    
    def urlBuilder():
        url="https://api.themoviedb.org/3/discover/movie?language=en-US&page=1"

        if 'general_title' in standardized_data and standardized_data['general_title']:
            url = "https://api.themoviedb.org/3/search/multi?"
            title = standardized_data['general_title']
            url += f"query={title}&language=en-US&page=1"
            if 'year' in standardized_data and standardized_data['year']:
                url += f"&year={standardized_data['year']}"
        elif 'movie_title' in standardized_data and standardized_data['movie_title']:
            url = "https://api.themoviedb.org/3/search/movie?"
            movie_title = standardized_data['movie_title']
            url += f"query={movie_title}&language=en-US&page=1"
            if 'year' in standardized_data and standardized_data['year']:
                url += f"&year={standardized_data['year']}"
        elif 'tvshow_title' in standardized_data and standardized_data['tvshow_title']:
            url = "https://api.themoviedb.org/3/search/tv?"
            tvshow_title = standardized_data['tvshow_title'] or standardized_data['similar_tvshows']
            url += f"query={tvshow_title}&language=en-US&page=1"
            if 'year' in standardized_data and standardized_data['year']:
                url += f"&year={standardized_data['year']}"
        elif 'person_name' in standardized_data and standardized_data['person_name']:
            url = "https://api.themoviedb.org/3/search/person?"
            person_name = standardized_data['person_name']
            url += f"query={person_name}&language=en-US&page=1"
        elif 'trending_movie' in standardized_data and standardized_data['trending_movie']:
            url = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"
        elif 'trending_tvshow' in standardized_data and standardized_data['trending_tvshow']:
            url = "https://api.themoviedb.org/3/trending/tv/week?language=en-US"
        elif 'trending_person' in standardized_data and standardized_data['trending_person']:
            url = "https://api.themoviedb.org/3/trending/person/week?language=en-US"
        elif 'top_rated_movie' in standardized_data and standardized_data['top_rated_movie']:
            url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US"
        elif 'top_rated_tvshow' in standardized_data and standardized_data['top_rated_tvshow']:
            url = "https://api.themoviedb.org/3/tv/top_rated?language=en-US"
        elif 'popular_person' in standardized_data and standardized_data['popular_person']:
            url = "https://api.themoviedb.org/3/person/popular?language=en-US"
        elif 'movie_or_tvshow' in standardized_data and standardized_data['movie_or_tvshow']:
            if standardized_data['movie_or_tvshow'] == "movie":
                url = "https://api.themoviedb.org/3/discover/movie?language=en-US&page=1"

                if 'genre' in standardized_data and standardized_data['genre']:
                    genre_prompt = f"Match the user's genre description '{standardized_data['genre']}' with the closest genre from this list: {movie_genreList}"
                    try:
                        model_response = llm.invoke(genre_prompt)
                        print(model_response.content)
                        matched_genre = model_response.content.strip()
                        genre_id = movie_genreList.get(matched_genre)
                    except Exception as e:
                        return jsonify({"error": "Error generating response"}), 500

                    if genre_id:
                        url += f"&with_genres={genre_id}"
                    if 'year' in standardized_data and standardized_data['year']:
                        url += f"&year={standardized_data['year']}"
            else:
                url = "https://api.themoviedb.org/3/discover/tv?language=en-US&page=1"
            
                if 'genre' in standardized_data and standardized_data['genre']:
                    genre_prompt = f"Match the user's genre description '{standardized_data['genre']}' with the closest genre from this list: {tvshow_genreList}"
                    try:
                        model_response = llm.invoke(genre_prompt)
                        print(model_response.content)
                        matched_genre = model_response.content.strip()
                        genre_id = tvshow_genreList.get(matched_genre)
                    except Exception as e:
                        return jsonify({"error": "Error generating response"}), 500

                    if genre_id:
                        url += f"&with_genres={genre_id}"
                    if 'year' in standardized_data and standardized_data['year']:
                        url += f"&year={standardized_data['year']}"

        return url
    
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
            return jsonify({"error": "Failed to fetch movie information"}), 500

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
            - Prioritize information from the 'Available Information'. 
            - If the 'Available Information' seems inadequate, use your internal knowledge about movies and TV shows.
            - Exclude any URLs from the response.
            Response:
            """

        try:    
            response = llm.invoke(prompt) 
            return response.content if response else "Error generating response"
        except Exception as e:
            print(e)
            return ""

    langchain_response = generate_langchain_response(user_query, info)

    langchain_response += "\n\n Disclaimer: All the information provided are from TMDB database and ChatGPT3.5."

    final_response = {"data": langchain_response}

    return jsonify(final_response)

app.run(port=5000, debug=True)




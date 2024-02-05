
from dotenv import load_dotenv

from flask import Flask, request, jsonify
import requests

from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI
from langchain.chains.api import tmdb_docs
from langchain.chains import APIChain

import os

load_dotenv('config.env')

openai_api_key = os.getenv('OPENAI_API_KEY')
tmdb_api_token = os.getenv('TMDB_API_TOKEN')

app = Flask(__name__)

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
            "movie": {"type": "string"},
            "year" : {"type": "string"}
        },
    }

    #LLM code
    llm = ChatOpenAI(openai_api_key = openai_api_key, temperature=0, model="gpt-3.5-turbo")
    chain = create_extraction_chain(schema, llm)

    try:
        data = chain.invoke(user_query)
    except Exception as e:
        return jsonify({"error": "Failed to process the query"}), 500

    print(data)

    if not data['text']:
        return jsonify({"error": "Requested information not available"}), 400
    
    extracted_data = data['text'][0]

    url = "https://api.themoviedb.org/3/search/movie?"

    if 'movie' in extracted_data and extracted_data['movie']:
        movie_title = extracted_data['movie']
        url += f"query={movie_title}&include_adult=false&language=en-US&page=1"

    if 'year' in extracted_data and extracted_data['year']:
        movie_year = extracted_data['year']
        url += f"&year={movie_year}"

    print(url)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        info = response.text
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch movie information"}), 500

    print(info)

    #generate user response
    def generate_langchain_response(user_query, info):
        prompt = f"User asked: {user_query}\n\nMovie Information: {info}\n\nResponse: "
        response = llm.invoke(prompt) 
        return response.content if response else "Error generating response"

    langchain_response = generate_langchain_response(user_query, info)

    final_response = {"data": langchain_response}

    return jsonify(final_response)

app.run(port=5000, debug=True)





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
    user_query = request.json['query']

    # #LLM code
    schema = {
        "properties": {
            "movie": {"type": "string"},
            "year" : {"type": "string"}
        },
    }

    llm = ChatOpenAI(openai_api_key = openai_api_key, temperature=0, model="gpt-3.5-turbo")

    #schema
    chain = create_extraction_chain(schema, llm)
    data = chain.run(user_query)

    print(data)
    
    url=""

    #hit tmdb api
    if('movie' in data[0]):
        url = f"https://api.themoviedb.org/3/search/movie?query={data[0]['movie']}&include_adult=false&language=en-US&page=1"
    if('year' in data[0]):
        url = url+"&year={year}"

    print(url)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api_token}"
    }

    response = requests.get(url, headers=headers)

    info = response.text

    # Assuming you have a function to generate a response using LangChain
    def generate_langchain_response(user_query, info):
        prompt = f"User asked: {user_query}\n\nMovie Information: {info}\n\nResponse: "
        response = llm.invoke(prompt) 
        return response

    # Generate a response
    langchain_response = generate_langchain_response(user_query, info)

    final_response = {"data": langchain_response.content}

    return jsonify(final_response)

app.run(port=5000)




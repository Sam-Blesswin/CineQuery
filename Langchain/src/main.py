from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    print(data)

    #LLM code
    
    response = {"data": "Processed data"}
    return jsonify(response)

app.run(port=5000)

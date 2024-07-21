from flask import Flask, request, jsonify
from youtube import getResponse, process_keyword  # Import the new function
from flask_cors import CORS
from groqFunctions import getKeywordsWithGroq
import json

from youtube_transcript import getTranscript

app = Flask(__name__)

CORS(app)

# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the Flask application!"

# Define a route to handle GET requests
@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'

# Define a route to handle POST requests
@app.route('/summary', methods=['GET'])
def echo():
    data = request.json
    print(str(data))
    keyword = data['keyword']  
    output_type = data['output_type']
    response = process_keyword(keyword, output_type)  
    return jsonify(response)




@app.route('/summary/v3', methods=['POST'])
def get_original_youtube_transcript():
    data = request.json

    url = data['youtube_link']
    output_type = data['output_type']
    transcript = getTranscript(url)
    response = getResponse(output_type, transcript)
    return jsonify(response)

@app.route('/friends/keywords', methods=['POST'])
def fetch_keywords():
    data = request.json
    print(type(data))
    overview = data["structured"]["overview"]
    response = getKeywordsWithGroq(overview)
    return jsonify(response)
    

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

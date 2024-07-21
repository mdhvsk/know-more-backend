from flask import Flask, request, jsonify
from youtube import process_keywords  
from paperwork import process_keywords_v2
from flask_cors import CORS
from groqFunctions import getKeywordsWithOpenAi

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
@app.route('/summary', methods=['POST'])
def echo():
    data = request.json
    print(data)
    keyword = data['words']  
    output_type = data['output_type']
    response = process_keywords(keyword, output_type)  
    return jsonify(response)

@app.route('/summaryV2', methods=['POST'])
def summary_v2():
    data = request.json
    print(data)
    keyword = data['words']  
    output_type = data['output_type']
    response = process_keywords(keyword, output_type)  
    return jsonify(response)

@app.route('/friends/keywords/openai', methods=['POST'])
def fetch_keywords_openai():
    data = request.json
    print(type(data))
    overview = data["structured"]["overview"]
    response = getKeywordsWithOpenAi(overview)
    return response

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from youtube_transcript import getTranscript, getResponse
app = Flask(__name__)

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
    url = data['youtube_link']
    output_type = data['output_type']
    transcript = getTranscript(url)
    response = getResponse(output_type, transcript)
    return jsonify(response)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
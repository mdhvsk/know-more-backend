from flask import Flask, request, jsonify
from youtube import process_keyword  # Import the new function
from flask_cors import CORS

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
    keyword = data['keyword']  
    output_type = data['output_type']
    response = process_keyword(keyword, output_type)  
    return jsonify(response)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import util
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    if request.method == 'POST':
        data = request.get_json()  # Expecting JSON data
        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])
    else:
        # If it's a GET request, use query parameters
        total_sqft = float(request.args.get('total_sqft'))
        location = request.args.get('location')
        bhk = int(request.args.get('bhk'))
        bath = int(request.args.get('bath'))

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    load_dotenv()  # Ensure to load the .env file
    port = int(os.getenv('FLASK_PORT', 5000))
    print(f"Starting Python Flask Server For Home Price Prediction on port {port}...")
    util.load_saved_artifacts()
    app.run(host="0.0.0.0", port=port)

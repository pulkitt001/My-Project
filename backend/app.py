from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas URI from .env file
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["convo_db"]  # 👈 You can name it anything
collection = db["conversations"]  # 👈 This is your collection

# Route: Home
@app.route('/')
def home():
    return "Flask app connected to MongoDB!"

# Route: Add a conversation (POST)
@app.route('/add', methods=['POST'])
def add_data():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

# Route: Get all conversations (GET)
@app.route('/get', methods=['GET'])
def get_data():
    documents = list(collection.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return jsonify(documents)

if __name__ == '__main__':
    app.run(debug=True)

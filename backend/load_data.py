import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load MongoDB URI from .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['ecommerce']  # database name

# Path to your CSV files
DATA_DIR = "data"

# Mapping of CSV file names to MongoDB collection names
csv_collections = {
    "distribution_centers.csv": "distribution_centers",
    "inventory_items.csv": "inventory_items",
    "order_items.csv": "order_items",
    "orders.csv": "orders",
    "products.csv": "products",
    "users.csv": "users"
}

# Function to load CSV to MongoDB
def load_csv(filename, collection_name):
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        if data:
            db[collection_name].insert_many(data)
            print(f"Inserted {len(data)} records into '{collection_name}' collection.")

# Loop through all files and insert
for csv_file, collection_name in csv_collections.items():
    load_csv(csv_file, collection_name)

print("✅ All data loaded successfully.")

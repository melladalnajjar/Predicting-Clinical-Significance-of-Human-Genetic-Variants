#########Phase 1 — MongoDB Ingestion & Exploration
import csv
from pymongo import MongoClient

# --- CONFIG ---
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "mydb"
COLLECTION_NAME = "mycollection"
FILE_PATH = "data.tsv"   # your TSV file
BATCH_SIZE = 5000        # adjust between 5k–10k for performance

# --- CONNECT ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

batch = []

with open(FILE_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")  # TSV uses tab delimiter

    for row in reader:
        # Convert row (OrderedDict) → normal dict
        doc = dict(row)
        batch.append(doc)

        # If batch is full → insert into MongoDB
        if len(batch) >= BATCH_SIZE:
            collection.insert_many(batch)
            batch = []  # reset batch

# Insert remaining rows
if batch:
    collection.insert_many(batch)

print("TSV ingestion completed successfully.")

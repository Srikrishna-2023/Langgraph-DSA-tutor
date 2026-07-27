"""
Day 4 — load seed_problems.json into ChromaDB.

Design decision: testcases stay in seed_problems.json only (source of truth).
ChromaDB holds id/topic/difficulty/description so we can search, then look up
the full problem (including testcases) from the JSON file using the id.
"""

import json
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

# get_or_create so re-running this script doesn't crash on "collection exists"
collection = client.get_or_create_collection("dsa_problems")

with open("problems/seed_problems.json") as f:
    data = json.load(f)

problems = data["problems"]

ids = []
documents = []
metadatas = []

for problem in problems:
    ids.append(problem["id"])

    # searchable text — topic + description combined, like the reference example
    documents.append(f"Topic: {problem['topic']}. {problem['description']}")

    # structured fields for filtering/retrieval — flat values only, no testcases here
    metadatas.append({
        "topic": problem["topic"],
        "difficulty": problem["difficulty"],
    })

collection.add(ids=ids, documents=documents, metadatas=metadatas)

print(f"Loaded {len(ids)} problems into ChromaDB.")

# quick retrieval test
results = collection.query(query_texts=["a problem about binary trees"], n_results=3)
print("\nTest query: 'a problem about binary trees'")
for id_, doc in zip(results["ids"][0], results["documents"][0]):
    print(f"  {id_}: {doc}")
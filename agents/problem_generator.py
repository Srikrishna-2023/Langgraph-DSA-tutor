import json
import random
import chromadb
from state import SessionState

# set up client/collection and problems_by_id dict here, outside the function
# (so it only loads once, not on every call)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("dsa_problems")
with open ("problems/seed_problems.json") as f:
    data = json.load(f)

problems_by_id = {problem["id"]: problem for problem in data["problems"]}
def problem_generator(state: SessionState) -> SessionState:
    topic = state.get("topic")
    difficulty = state.get("difficulty")

    results = collection.get(
        where={"$and": [{"topic": topic}, {"difficulty": difficulty}]}
    )

    matching_ids = results["ids"]
    if not matching_ids:
        state["current_problem"] = None
        state.setdefault("session_log", []).append(
            {"node": "problem_generator", "result": "no_match", "topic": topic, "difficulty": difficulty}
    )
        return state  # no matching problems found
    else:
        selected_id=random.choice(matching_ids)
        selected_problem=problems_by_id[selected_id]
        state["current_problem"] = {
            "id": selected_problem["id"],
            "statement": selected_problem["description"],
            "test_cases": selected_problem["testcases"],
        }
    session_log_entry = {"node": "problem_generator", "problem_id": selected_problem["id"]}
    state.setdefault("session_log", []).append(session_log_entry)   
    return state
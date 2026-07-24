"""
Day 1, Week 2 — just confirm we can call Ollama from Python.
No LangGraph, no state, nothing fancy. Get this working first.
"""

import ollama

# swap "llama3" for whatever model `ollama list` shows you actually have
MODEL_NAME = "llama3"

response = ollama.chat(
    model=MODEL_NAME,
    messages=[
        {"role": "user", "content": "Classify this into one of: new_problem, review_solution, hint_request. Text: 'give me a medium two pointer problem'. Reply with only the label."}
    ],
)

print("Full response object:")
print(response)
print()
print("Just the model's reply:")
print(response["message"]["content"])
"""
CLI loop to interactively test the graph.

Try inputs like:
  "give me a medium two-pointer problem"
  "I want a hint"
  "review my solution"      (won't have real user_code yet — that's fine for now)
type 'quit' to exit.
"""

from graph import build_graph

app = build_graph()

print("DSA Agent (Week 1 skeleton) — type 'quit' to exit\n")

while True:
    text = input(" ")
    if text.strip().lower() == "quit":
        break

    initial_state = {
        "user_request": text,
        "hint_history": [],
        "hint_level": 0,
        "weak_topics": [],
        "session_log": [],
    }

    result = app.invoke(initial_state)
    print(f"\n[final intent: {result['intent']}]\n")
    if result.get("current_problem"):
        print(f"\nProblem: {result['current_problem']['statement']}")
        print(f"Test cases: {result['current_problem']['test_cases']}\n")
    else:
        print("\nNo matching problem found.\n")
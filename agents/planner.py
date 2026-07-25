"""
Planner agent.

Week 1 version: no LLM call yet. Uses simple keyword matching to decide
intent, just so we can wire up the graph and test routing end-to-end.
We'll swap this for a real LLM call in Week 2.
"""

from state import SessionState
import ollama

def plan(state: SessionState) -> SessionState:
    text = state["user_request"]
    Model="llama3"
    response=ollama.chat(Model,
    messages=[
        {"role": "user", "content": f"Classify this into one of: new_problem, review_solution, hint_request. Text: '{text}'. Reply with only the label."}],
    )
    state["intent"] = response.message.content.strip()
    if state["intent"] == "new_problem":
        for level in ("easy", "medium", "hard"):
            if level in text:
                state["difficulty"] = level
                break
        else:
            state["difficulty"] = "medium"
        
        known_topics = [
                    "two-pointer", "two pointer", "dutch national flag", "binary search",
                    "linked list", "tree", "stack", "queue", "monotonic stack",
                    "dynamic programming", "dp",
                ]
        state["topic"] = next((t for t in known_topics if t in text), "unspecified")
    # if "hint" in text:
    #     state["intent"] = "hint_request"

    # elif "review" in text or "check my" in text or state.get("user_code"):
    #     state["intent"] = "review_solution"

    # else:
    #     # default: treat as a request for a new problem
    #     state["intent"] = "new_problem"

        # very naive topic/difficulty extraction for now — Week 2 will
        # replace this with a real LLM call that does this properly
        

    state.setdefault("session_log", []).append(
        {"node": "planner", "decision": state["intent"]}
    )
    return state
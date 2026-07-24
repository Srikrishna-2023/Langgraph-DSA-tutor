"""
Wires up the StateGraph: nodes + conditional routing edges.

Routing logic (from spec):
  Planner -> Problem-Generator   if intent == "new_problem"
  Planner -> Code-Execution      if intent == "review_solution"
  Planner -> Critic              if intent == "hint_request"

  Code-Execution -> Critic            if a test failed
  Code-Execution -> Memory-Updater    if all tests passed

  Critic -> Memory-Updater
  Problem-Generator -> END (waits for the user's attempt)
"""
from langgraph.graph import StateGraph, END

from state import SessionState
from agents.planner import plan
from agents.stubs import problem_generator, code_executor, critic, memory_updater


def route_from_planner(state: SessionState) -> str:
    return {
        "new_problem": "problem_generator",
        "review_solution": "code_executor",
        "hint_request": "critic",
    }[state["intent"]]


def route_from_execution(state: SessionState) -> str:
    return "critic" if not state["execution_result"]["passed"] else "memory_updater"


def build_graph():
    graph = StateGraph(SessionState)

    graph.add_node("planner", plan)
    graph.add_node("problem_generator", problem_generator)
    graph.add_node("code_executor", code_executor)
    graph.add_node("critic", critic)
    graph.add_node("memory_updater", memory_updater)

    graph.set_entry_point("planner")

    graph.add_conditional_edges("planner", route_from_planner)
    graph.add_conditional_edges("code_executor", route_from_execution)

    graph.add_edge("problem_generator", END)
    graph.add_edge("critic", "memory_updater")
    graph.add_edge("memory_updater", END)

    return graph.compile()
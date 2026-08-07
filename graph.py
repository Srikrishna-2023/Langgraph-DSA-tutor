"""
Wires up the StateGraph: nodes + conditional routing edges.
All 5 nodes are now real (no more stubs.py).
"""

from langgraph.graph import StateGraph, END

from state import SessionState
from agents.planner import plan
from agents.problem_generator import problem_generator
from agents.executor import code_executor
from agents.stubs import critic
from agents.stubs import memory_updater


def route_from_planner(state: SessionState) -> str:
    return {
        "new_problem": "problem_generator",
        "review_solution": "code_executor",
        "hint_request": "critic",
    }[state["intent"]]


def route_from_execution(state: SessionState) -> str:
    result = state.get("execution_result")
    if result and result.get("passed"):
        return "memory_updater"
    return "critic"


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
"""
Stand-in nodes for Problem-Generator, Code-Execution, Critic, and Memory-Updater.

These just print what they *would* do and return canned data, so we can
test the graph's routing logic before building each agent for real.
Each of these gets replaced with a real implementation in later weeks.
"""

from state import SessionState


def problem_generator(state: SessionState) -> SessionState:
    print(f"[Problem-Generator] would fetch a {state.get('difficulty')} "
          f"{state.get('topic')} problem here")
    state["current_problem"] = {
        "id": "stub-001",
        "statement": "(stub) Two Sum — return indices of two numbers that add to target",
        "test_cases": [{"input": [2, 7, 11, 15], "target": 9, "expected": [0, 1]}],
    }
    state.setdefault("session_log", []).append({"node": "problem_generator"})
    return state


def code_executor(state: SessionState) -> SessionState:
    print("[Code-Execution] would run user_code against test cases here")
    state["execution_result"] = {"passed": False, "failed_case": 0, "error": None}
    state.setdefault("session_log", []).append({"node": "code_executor"})
    return state


def critic(state: SessionState) -> SessionState:
    level = state.get("hint_level", 0) + 1
    print(f"[Critic] would generate a level-{level} hint here")
    state["hint_level"] = level
    state.setdefault("hint_history", []).append(f"(stub hint level {level})")
    state.setdefault("session_log", []).append({"node": "critic", "hint_level": level})
    return state


def memory_updater(state: SessionState) -> SessionState:
    print("[Memory-Updater] would write session_log to persistent memory here")
    print(f"  session_log so far: {state.get('session_log')}")
    return state
"""
Stand-in nodes for Problem-Generator, Code-Execution, Critic, and Memory-Updater.

These just print what they *would* do and return canned data, so we can
test the graph's routing logic before building each agent for real.
Each of these gets replaced with a real implementation in later weeks.
"""

from state import SessionState





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
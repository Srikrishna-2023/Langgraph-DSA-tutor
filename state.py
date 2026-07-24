"""
Shared state object passed between all agent nodes in the graph.
"""

from typing import TypedDict, Optional


class SessionState(TypedDict, total=False):
    # what the user typed
    user_request: str

    # set by Planner
    intent: str                    # "new_problem" | "review_solution" | "hint_request"
    topic: Optional[str]
    difficulty: Optional[str]

    # set by Problem-Generator
    current_problem: Optional[dict]

    # set by user / caller before Code-Execution
    user_code: Optional[str]

    # set by Code-Execution
    execution_result: Optional[dict]

    # set by Critic
    hint_history: list
    hint_level: int

    # loaded from memory at session start
    weak_topics: list

    # appended to throughout, flushed to memory store at end
    session_log: list
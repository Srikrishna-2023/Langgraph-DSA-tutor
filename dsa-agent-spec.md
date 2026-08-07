# Multi-Agent DSA Interview Prep System — Architecture Spec

## Overview
A LangGraph-based multi-agent system that generates DSA problems, executes/tests your
solutions, gives Socratic hints instead of answers, and tracks weak topics over time.

---

## 1. Agents (Graph Nodes)

### Planner
- **Input**: raw user request (e.g. "give me a medium two-pointer problem", "review my solution")
- **Job**: classify intent, decide which node(s) to route to next
- **Output**: routing decision + structured sub-task

### Problem-Generator
- **Input**: topic, difficulty, exclusion list (problems already seen)
- **Job**: retrieve or generate a DSA problem matching constraints
- **Output**: problem statement, constraints, example test cases, hidden test cases
- **Data source**: vector DB (ChromaDB) of curated problems, or LLM generation validated
  against a schema

### Code-Execution
- **Input**: user's code submission + test cases from Problem-Generator
- **Job**: run code in a sandbox (Docker container, resource-limited), collect pass/fail,
  runtime, and any errors
- **Output**: structured result (passed/failed test cases, exceptions, runtime)

### Critic (Socratic Hints)
- **Input**: problem, user's code or approach, execution results
- **Job**: generate a graduated hint — never the full answer unless explicitly asked
  - Level 1: nudge toward the right pattern ("what happens at the boundaries?")
  - Level 2: point at the specific bug or missing case
  - Level 3: pseudocode-level hint (only if user asks again)
- **Output**: one hint + hint level used

### Memory-Updater
- **Input**: topic, outcome (solved/struggled/failed), hints used, time taken
- **Job**: update persistent user model — weak topics, hint-dependency per topic,
  spaced-repetition schedule
- **Output**: write to memory store

---

## 2. State Object (shared across graph)

```python
class SessionState(TypedDict):
    user_request: str
    intent: str                    # "new_problem" | "review_solution" | "hint_request"
    topic: str | None
    difficulty: str | None
    current_problem: dict | None
    user_code: str | None
    execution_result: dict | None
    hint_history: list[str]
    hint_level: int
    weak_topics: list[str]         # loaded from memory at session start
    session_log: list[dict]        # for memory update at end
```

---

## 3. Routing Logic (Edges)

```
START -> Planner

Planner -> Problem-Generator   [if intent == "new_problem"]
Planner -> Code-Execution      [if intent == "review_solution" and user_code present]
Planner -> Critic              [if intent == "hint_request"]

Problem-Generator -> END       [returns problem to user, waits for their attempt]

Code-Execution -> Critic       [if any test failed]
Code-Execution -> Memory-Updater [if all tests passed]

Critic -> Memory-Updater       [after hint given, log hint usage]

Memory-Updater -> END
```

Use a `conditional_edge` on the Planner node keyed off `intent`, and a conditional edge
on Code-Execution keyed off pass/fail.

---

## 4. Memory Schema (persistent, SQLite or ChromaDB)

```sql
-- topics table
topic_name TEXT PRIMARY KEY
attempts INTEGER
solved INTEGER
avg_hints_used REAL
last_attempted TIMESTAMP
mastery_score REAL   -- derived: solved/attempts weighted by hint reliance

-- sessions table (for history/analytics)
session_id TEXT
topic TEXT
outcome TEXT          -- solved | struggled | failed
hints_used INTEGER
time_taken_seconds INTEGER
timestamp TIMESTAMP
```

`mastery_score` feeds back into Problem-Generator's topic-selection weighting —
lower mastery topics get surfaced more often (spaced repetition style).

---

## 5. Tool Schemas (for LangGraph tool-calling)

```python
# code execution tool
{
  "name": "execute_code",
  "input": {"code": str, "language": "python", "test_cases": list[dict]},
  "output": {"passed": bool, "results": list[dict], "stdout": str, "stderr": str, "runtime_ms": float}
}

# problem retrieval tool
{
  "name": "search_problems",
  "input": {"topic": str, "difficulty": str, "exclude_ids": list[str]},
  "output": {"problem_id": str, "statement": str, "constraints": str, "test_cases": list[dict]}
}
```

---

## 6. Project Structure

```
dsa-agent/
├── agents/
│   ├── planner.py
│   ├── problem_generator.py
│   ├── code_executor.py
│   ├── critic.py
│   └── memory_updater.py
├── graph.py              # LangGraph StateGraph wiring
├── memory/

│   ├── schema.sql
│   └── store.py          # SQLite/ChromaDB interface
├── sandbox/
│   └── docker_runner.py  # isolated code execution
├── problems/
│   └── seed_problems.json
├── cli.py                # entrypoint
├── requirements.txt
└── README.md
```

---

## 7. Build Order (suggested)

1. **Week 1**: State object, Planner node, hardcoded routing, CLI loop (no real LLM calls yet — stub responses)
2. **Week 2**: Problem-Generator with seed problem bank (20-30 problems across your known weak topics), wire in real LLM calls
3. **Week 3**: Code-Execution sandbox (start with subprocess + resource limits, upgrade to Docker), Critic agent with hint levels
4. **Week 4**: Memory layer, spaced-repetition weighting, polish CLI or add minimal FastAPI wrapper

---

## 8. Model Choice Notes

- **Planner / Critic**: use an API-based model (Claude) — these need real reasoning quality
- **Problem-Generator**: can use local Ollama model if you want partial offline capability,
  but quality of generated test cases will be weaker — consider a hybrid (LLM generates,
  a validator step checks test cases   actually match the problem statement)

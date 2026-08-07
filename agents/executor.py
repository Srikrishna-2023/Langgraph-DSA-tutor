"""
code_executor agent.

Takes state["user_code"] and state["current_problem"] (with its test_cases
and function_name), runs the code against EACH test case inside Docker,
and builds a structured state["execution_result"].
"""

import docker
import requests

client = docker.from_env()

TEMP_CODE_PATH = "agents/tempcode.py"
CONTAINER_CODE_PATH = "/code/tempcode.py"
HOST_MOUNT_FOLDER = r"C:\Users\srikr\Desktop\Agentic System\agents"


def code_executor(state):
    # --- unsupported-problem check (unchanged from before) ---
    if state["current_problem"].get("_note"):
        state["execution_result"] = {
            "passed": False,
            "status": "skipped",
            "error": "Execution skipped due to problem note: " + state["current_problem"]["_note"],
        }
        state.setdefault("session_log", []).append(
            {"node": "code_executor", "result": "skipped", "reason": "unavailable problem"}
        )
        return state

    test_cases = state["current_problem"]["test_cases"]
    function_name = state["current_problem"]["function_name"]
    user_code = state["user_code"]

    results = []

    for test_case in test_cases:
        # Step 1: everything except "expected" is an input
        inputs = {}
        for key in test_case:
            if key != "expected":
                inputs[key] = test_case[key]

        # Step 2: turn those values into a comma-separated arg string
        args_string = ", ".join(map(str, list(inputs.values())))

        # Step 3: pull out expected separately
        expected = test_case["expected"]

        # Step 4: build the runner snippet for THIS test case
        runner_code = f"""
result = {function_name}({args_string})
print(result == {expected})
"""

        # Step 5: combine and write to file
        full_code = user_code + "\n" + runner_code
        with open(TEMP_CODE_PATH, "w") as f:
            f.write(full_code)

        # Step 6: run in Docker, same pattern as Day 11
        test_result = {"test_case": test_case}

        try:
            container = client.containers.run(
                image="dsa-sandbox-base",
                command=["python", CONTAINER_CODE_PATH],
                volumes={HOST_MOUNT_FOLDER: {"bind": "/code", "mode": "ro"}},
                mem_limit="100m",
                detach=True,
            )
        except Exception as e:
            test_result["passed"] = False
            test_result["error"] = f"Failed to start container: {e}"
            results.append(test_result)
            continue  # move on to the next test case

        try:
            exit_info = container.wait(timeout=5)
            logs = container.logs().decode("utf-8").strip()

            # Step 7: decide pass/fail
            if exit_info.get("StatusCode") != 0:
                # code crashed (syntax error, exception, etc.)
                test_result["passed"] = False
                test_result["error"] = logs  # logs hold the traceback in this case
            elif logs == "True":
                test_result["passed"] = True
            else:
                # ran fine, but produced False (wrong answer) or unexpected output
                test_result["passed"] = False
                test_result["error"] = f"Unexpected output: {logs}"

        except requests.exceptions.ConnectionError:
            test_result["passed"] = False
            test_result["error"] = "Execution timed out"

        finally:
            try:
                container.stop()
            except Exception:
                pass
            try:
                container.remove()
            except Exception:
                pass

        # Step 8: record this test case's result
        results.append(test_result)

    # --- after the loop: summarize into state["execution_result"] ---
    total = len(results)
    passed_count = sum(1 for r in results if r.get("passed"))

    state["execution_result"] = {
        "passed": passed_count == total,
        "status": "completed",
        "total_tests": total,
        "passed_tests": passed_count,
        "details": results,
    }

    state.setdefault("session_log", []).append(
        {"node": "code_executor", "result": f"{passed_count}/{total} passed"}
    )

    return state


if __name__ == "__main__":
    fake_state = {
        "user_code": """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
""",
        "current_problem": {
            "test_cases": [
                {"array": [2, 7, 11, 15], "target": 9, "expected": [0, 1]},
                {"array": [3, 2, 4], "target": 6, "expected": [1, 2]},
            ],
            "function_name": "two_sum",
            "_note": None,
        },
    }
    result_state = code_executor(fake_state)
    print(result_state["execution_result"])
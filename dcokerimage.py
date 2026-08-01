import docker
client=docker.from_env()
user_code = """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]


"""
test_case = {"array": [2, 7, 11, 15], "target": 9, "expected": [0, 1]}
function_name = "two_sum"
inputs = {}
for key in test_case:
    if key != "expected":
        inputs[key] = test_case[key]
args_string = ", ".join(map(str, list(inputs.values())))
print(args_string)

function_name = "two_sum"
array = [2, 7, 11, 15]
target = 9
expected = [0, 1]
runner_code = runner_code = f"""
result = {function_name}({args_string})
print(result == {expected})
"""
full_code = user_code + "\n" + runner_code
with open("agents/tempcode.py", "w") as f:
    f.write(full_code)
container = client.containers.run(
    image="dsa-sandbox-base",
    command=["python", "/code/tempcode.py"],
    volumes={r"C:\Users\srikr\Desktop\Agentic System\agents": {"bind": "/code", "mode": "ro"}},
    mem_limit="100m",
    detach=True
)

try:
    result = container.wait(timeout=5)
    logs = container.logs()
    print("Output:", logs.decode("utf-8"))
    print("Finished normally:", result)
except Exception as e:
    print("Exception type:", type(e))
    print("Exception message:", e)
finally:
    try:
        container.stop()
        print("Container stopped successfully")
    except Exception as e:
        print("stop() failed:", type(e), e)

    try:
        container.remove()
        print("Container removed successfully")
    except Exception as e:
        print("remove() failed:", type(e), e)
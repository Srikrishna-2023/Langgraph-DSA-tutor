import docker
client=docker.from_env()

user_code = """
while True:
    pass
"""
with open("agents/tempcode.py", "w") as f:
    f.write(user_code)
output=client.containers.run(image="dsa-sandbox-base",command=["python", "/code/tempcode.py"],volumes={r"C:\Users\srikr\Desktop\Agentic System\agents": {"bind": "/code", "mode": "ro"} },
mem_limit="100m",
remove=True
)

print(output.decode("utf-8"))
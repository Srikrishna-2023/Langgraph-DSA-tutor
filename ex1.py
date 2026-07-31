import docker
client=docker.from_env()

container = client.containers.run(
    image="dsa-sandbox-base",
    command=["python", "/code/tempcode.py"],
    volumes={r"C:\Users\srikr\Desktop\Agentic System\agents": {"bind": "/code", "mode": "ro"}},
    mem_limit="100m",
    detach=True
)

try:
    result = container.wait(timeout=5)
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
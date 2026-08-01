full_code = user_code + "\n" + runner_code

with open("agents/tempcode.py", "w") as f:
    f.write(full_code)
test_case = {"target": 9, "array": [2, 7, 11, 15], "expected": [0, 1]}

inputs = {}
for key in test_case:
    if key != "expected":
        inputs[key] = test_case[key]

print(inputs)
print(list(inputs.values()))
inputs = {"target": 9, "array": [2, 7, 11, 15]}
args_string = ", ".join(map(str, list(inputs.values())))
print(args_string)
import subprocess
import sys

try:
    result = subprocess.run(
        [sys.executable, 'C:/Users/srikr/Desktop/Agentic System/agents/tempcode.py'],
        capture_output=True, text=True, timeout=5
    )
    print(result.stdout)
    print(result.stderr)
    print(result.returncode)
except subprocess.TimeoutExpired:
    print("Execution timed out.")
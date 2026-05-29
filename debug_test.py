import sys
sys.path.append('examples/05_pr_security_agent')

from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent

agent = create_agent()

initial_state = {
    "pr_id": "PR-CLEAN",
    "diff_content": "def hello():\n    return 'world'\n\n# This is a clean change",
    "steps": [],
    "security_issues": [],
    "quality_issues": [],
    "loop_count": 0,
    "status": "start"
}

print("Initial state:", initial_state)

# Use GraphRunCapture to capture the execution
with GraphRunCapture(agent, initial_state) as captured_run:
    print("Captured run keys:", list(captured_run.keys()))
    print("Nodes:", captured_run.get("nodes", []))
    print("Final state:", captured_run.get("final_state"))

    result = agent.invoke(initial_state)
    print("Result:", result)
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
    print("Inside context manager - BEFORE invoke:")
    print("  captured_run keys:", list(captured_run.keys()))
    print("  captured_run nodes:", captured_run.get("nodes", "KEY MISSING"))

    result = agent.invoke(initial_state)

    print("Inside context manager - AFTER invoke:")
    print("  result:", result)
    print("  captured_run keys:", list(captured_run.keys()))
    print("  captured_run nodes:", captured_run.get("nodes", "KEY MISSING"))
    if 'nodes' in captured_run:
        print("  nodes content:", captured_run['nodes'])

    # Test the assertion function directly
    from langgraph_evals.core.assertions import assert_node_called
    try:
        assert_node_called(captured_run, "supervisor")
        print("  ASSERTION PASSED: supervisor was called")
    except AssertionError as e:
        print("  ASSERTION FAILED:", str(e))
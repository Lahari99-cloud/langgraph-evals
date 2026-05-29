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
    result = agent.invoke(initial_state)

    print("Result:", result)
    print("Nodes in captured_run:", captured_run.get("nodes", []))

    # Let's examine each node to see what's happening
    nodes = captured_run.get("nodes", [])
    for i, node in enumerate(nodes):
        print(f"  Node {i}: {node}")
        if isinstance(node, dict):
            print(f"    Type: dict, keys: {list(node.keys())}")
            for k, v in node.items():
                print(f"      {k}: {v} (type: {type(v)})")
        else:
            print(f"    Type: {type(node)}")
            # Try to get attributes
            for attr in ['name']:
                if hasattr(node, attr):
                    print(f"      {attr}: {getattr(node, attr)}")

    # Now test the classifier
    from langgraph_evals.core.failure_classifier import FailureClassifier
    classifier = FailureClassifier()
    failure_result = classifier.classify(nodes)
    print(f"Failure result: {failure_result}")

    if failure_result:
        print(f"Failure evidence: {failure_result.evidence}")
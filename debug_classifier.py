# Test what the classifier actually sees in the working example
import sys
import os

# Add the examples directory to path
examples_path = os.path.join(os.getcwd(), 'examples/04_langgraph_integration')
sys.path.append(examples_path)

from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent
from langgraph_evals.core.failure_classifier import FailureClassifier

agent = create_agent()

# Test with the working example
initial_state = {
    "input": "hello world",
    "steps": [],
    "result": None
}

print("=== Testing Working Example ===")
print("Initial state:", initial_state)

# Use GraphRunCapture to capture the execution
with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    print("Result:", result)
    print("Nodes:", captured_run.get("nodes", []))

    # Test the classifier
    classifier = FailureClassifier()
    nodes = captured_run["nodes"]
    print("Nodes passed to classifier:", nodes)

    # Let's manually trace what the classifier sees
    print("Manual inspection of classifier logic:")
    for i, node in enumerate(nodes):
        print(f"  Node {i}: {node}")
        print(f"    Type: {type(node)}")
        if isinstance(node, dict):
            print(f"    Keys: {list(node.keys())}")
            print(f"    node.get('node_name'): {node.get('node_name')}")
            print(f"    node.get('name'): {node.get('name')}")
        else:
            print(f"    Hasattr name: {hasattr(node, 'name')}")
            if hasattr(node, 'name'):
                print(f"    node.name: {getattr(node, 'name')}")

    failure_result = classifier.classify(nodes)
    print(f"Failure result: {failure_result}")

print("\n=== Testing Our New Example ===")
# Add the PR security agent directory to path
pr_security_path = os.path.join(os.getcwd(), 'examples/05_pr_security_agent')
sys.path.append(pr_security_path)
from agent import create_agent as create_pr_agent

agent = create_pr_agent()

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
    print("Nodes:", captured_run.get("nodes", []))

    # Test the classifier
    classifier = FailureClassifier()
    nodes = captured_run["nodes"]
    print("Nodes passed to classifier:", nodes)

    # Let's manually trace what the classifier sees
    print("Manual inspection of classifier logic:")
    for i, node in enumerate(nodes):
        print(f"  Node {i}: {node}")
        print(f"    Type: {type(node)}")
        if isinstance(node, dict):
            print(f"    Keys: {list(node.keys())}")
            print(f"    node.get('node_name'): {node.get('node_name')}")
            print(f"    node.get('name'): {node.get('name')}")
        else:
            print(f"    Hasattr name: {hasattr(node, 'name')}")
            if hasattr(node, 'name'):
                print(f"    node.name: {getattr(node, 'name')}")

    failure_result = classifier.classify(nodes)
    print(f"Failure result: {failure_result}")
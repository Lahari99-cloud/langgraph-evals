# Final test to check the classifier issue
import sys
import os
from collections import Counter

# Add the examples directory to path
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/05_pr_security_agent'))

# Test our example with a fresh import
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

print("Testing our PR security agent...")

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    nodes = captured_run["nodes"]

    print(f"Number of nodes: {len(nodes)}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node}")

    # Test what the classifier sees
    print("\nTesting classifier...")
    from langgraph_evals.core.failure_classifier import FailureClassifier
    classifier = FailureClassifier()

    # Let's manually step through what the classifier does
    print("Manual trace of classifier logic:")
    print(f"  max_loops (default): {classifier.__class__.__dict__.get('classify', lambda x: None).__defaults__[2] if hasattr(classifier.__class__.__dict__.get('classify', lambda x: None), '__defaults__') else '3 (from signature)'}")

    # Check what trace[-1].get("node_name") returns
    if nodes:
        last_node = nodes[-1].get("node_name")
        print(f"  trace[-1].get('node_name'): {last_node}")
        print(f"  trace[-1]: {nodes[-1]}")
        print(f"  trace[-1].get('name'): {nodes[-1].get('name')}")

    # Check the counts
    counts = Counter(t.get("node_name") for t in nodes)
    print(f"  counts from t.get('node_name'): {counts}")

    # Check what t.get('name') gives us
    name_counts = Counter(t.get("name") for t in nodes)
    print(f"  counts from t.get('name'): {name_counts}")

    # Now call the actual classifier
    failure_result = classifier.classify(nodes)
    print(f"\nActual failure result: {failure_result}")

    if failure_result:
        print(f"  Evidence: {failure_result.evidence}")
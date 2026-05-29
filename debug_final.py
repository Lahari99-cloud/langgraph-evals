# Final debug to see exactly what's in the nodes for the failing test

import sys
import os

# Test our example
print("=== DEBUGGING THE FAILING TEST ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/05_pr_security_agent'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent

agent = create_agent()
initial_state = {
    "pr_id": "PR-CLEAN",
    "diff_content": "def hello():\n    return 'world'\n\n# This is a clean change that includes testing\n",
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
    print()

    nodes = captured_run["nodes"]
    print(f"Number of nodes: {len(nodes)}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node}")
        if isinstance(node, dict):
            print(f"      Keys: {sorted(list(node.keys()))}")
            for k in ['name', 'node_name']:
                val = node.get(k, 'KEY_NOT_FOUND')
                print(f"      .get('{k}'): {repr(val)}")
        print()

    # Test what the classifier sees
    from langgraph_evals.core.failure_classifier import FailureClassifier
    classifier = FailureClassifier()

    print("--- Classifier Analysis ---")
    print(f"nodes: {nodes}")

    # Check last_node
    if nodes:
        last_node = nodes[-1].get("node_name")
        print(f"trace[-1].get('node_name'): {last_node}")
        print(f"trace[-1]: {nodes[-1]}")
        print(f"trace[-1].get('name'): {nodes[-1].get('name')}")

    # Check node_name counts
    node_name_values = [t.get("node_name") for t in nodes]
    print(f"t.get('node_name') for each t: {node_name_values}")
    from collections import Counter
    node_name_counts = Counter(t.get("node_name") for t in nodes)
    print(f"Counter(t.get('node_name')): {node_name_counts}")

    # Check name counts
    name_values = [t.get("name") for t in nodes]
    print(f"t.get('name') for each t: {name_values}")
    name_counts = Counter(t.get("name") for t in nodes)
    print(f"Counter(t.get('name')): {name_counts}")

    # Test the actual classifier
    failure_result = classifier.classify(nodes)
    print(f"\nActual failure result: {failure_result}")

    # Let's trace through the classifier logic manually with the CORRECT key
    print("\n--- Manual trace with CORRECT key ('name') ---")
    if nodes:
        last_node_name = nodes[-1].get("name")
        print(f"Last node name (using 'name'): {last_node_name}")

        name_counts_correct = Counter(t.get("name") for t in nodes)
        print(f"Node name counts (using 'name'): {name_counts_correct}")

        max_loops = 3
        loop_detected = False
        for node, count in name_counts_correct.items():
            if count > max_loops:
                print(f"LOOP DETECTED: Node '{node}' appears {count} times (>{max_loops})")
                loop_detected = True

        if not loop_detected:
            print("No loop overflow detected with correct key")

        # Check premature termination
        expected_end_node = "END"
        if last_node_name and last_node_name.upper() != "END":
            print(f"Would PREMATURE_TERMINATE: last_node='{last_node_name}' != 'END'")
        else:
            print(f"No premature termination: last_node='{last_node_name}' is END or None")
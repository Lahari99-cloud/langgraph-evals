# Check what's actually happening in the working example

import sys
import os

# Test working example
print("=== WORKING EXAMPLE NODES ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent

agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    nodes = captured_run["nodes"]
    print(f"Nodes: {nodes}")

    # Let's see what the classifier actually gets
    from langgraph_evals.core.failure_classifier import FailureClassifier
    classifier = FailureClassifier()

    print("\n--- What the classifier sees ---")
    print(f"trace: {nodes}")

    # Manual trace of classifier logic
    print(f"\ntrace[-1]: {nodes[-1]}")
    print(f"trace[-1].get('node_name'): {nodes[-1].get('node_name')}")
    print(f"trace[-1].get('name'): {nodes[-1].get('name')}")

    # The actual computation in classifier
    last_node = nodes[-1].get("node_name")
    print(f"\nlast_node = trace[-1].get('node_name'): {last_node}")

    counts = [t.get("node_name") for t in nodes]
    print(f"t.get('node_name') for each t: {counts}")

    from collections import Counter
    counter_result = Counter(t.get("node_name") for t in nodes)
    print(f"Counter(t.get('node_name')): {counter_result}")

    # Check if any count > max_loops (default 3)
    max_loops = 3
    print(f"\nChecking for counts > {max_loops}:")
    for node, count in counter_result.items():
        print(f"  '{node}': {count} > {max_loops}? {count > max_loops}")

    # Now test the actual classifier
    failure_result = classifier.classify(nodes)
    print(f"\nActual classifier result: {failure_result}")
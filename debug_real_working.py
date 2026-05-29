# Debug what the ACTUAL working example produces in the captured_run

import sys
import os

# Test working example with FULL debug
print("=== WORKING EXAMPLE FULL DEBUG ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent

agent = create_working_agent()
initial_state = {"input": "hello world", "steps": [], "result": None}

print("Initial state:", initial_state)

# Use GraphRunCapture to capture the execution
with GraphRunCapture(agent, initial_state) as captured_run:
    print("BEFORE invoke - captured_run keys:", list(captured_run.keys()))
    if 'nodes' in captured_run:
        print("BEFORE invoke - nodes:", captured_run['nodes'])
    else:
        print("BEFORE invoke - nodes KEY MISSING")

    result = agent.invoke(initial_state)

    print("AFTER invoke - result:", result)
    print("AFTER invoke - captured_run keys:", list(captured_run.keys()))

    if 'nodes' in captured_run:
        nodes = captured_run['nodes']
        print("AFTER invoke - nodes:", nodes)
        print("AFTER invoke - number of nodes:", len(nodes))
        for i, node in enumerate(nodes):
            print(f"  Node {i}: {node}")
            print(f"    Type: {type(node)}")
            if isinstance(node, dict):
                print(f"    Keys: {list(node.keys())}")
                for k, v in node.items():
                    print(f"      {k}: {repr(v)}")
    else:
        print("AFTER invoke - nodes KEY MISSING")

    # Test the classifier
    from langgraph_evals.core.failure_classifier import FailureClassifier
    classifier = FailureClassifier()

    if 'nodes' in captured_run:
        failure_result = classifier.classify(captured_run["nodes"])
        print("Failure result:", failure_result)
    else:
        print("No nodes to classify")
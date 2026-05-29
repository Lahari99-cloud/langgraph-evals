# Debug what the classifier actually does with the working example data

import sys
import os

# Test working example
print("=== WORKING EXAMPLE CLASSIFIER DEBUG ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent
from langgraph_evals.core.failure_classifier import FailureClassifier

agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    nodes = captured_run["nodes"]
    print(f"nodes: {nodes}")

    classifier = FailureClassifier()

    # Let's manually trace through the classifier logic with the actual parameters used in the test
    print("\n--- Manual trace with actual test parameters ---")
    trace = nodes
    expected_end_node = "END"  # This is the default
    max_loops = 3  # This is the default
    model_token_limit = 8192  # This is the default

    print(f"trace: {trace}")
    print(f"expected_end_node: {expected_end_node}")
    print(f"max_loops: {max_loops}")
    print(f"model_token_limit: {model_token_limit}")

    # Check if trace is empty
    if not trace:
        print("TRACE IS EMPTY -> PREMATURE_TERMINATION")
    else:
        print("TRACE NOT EMPTY")

        # Check last_node = trace[-1].get("node_name")
        last_node = trace[-1].get("node_name")
        print(f"last_node = trace[-1].get('node_name'): {last_node}")
        print(f"  trace[-1]: {trace[-1]}")
        print(f"  trace[-1].get('node_name'): {trace[-1].get('node_name')}")
        print(f"  trace[-1].get('name'): {trace[-1].get('name')}")

        # Check the WRONG_BRANCH condition first
        print(f"\nChecking WRONG_BRANCH condition:")
        print(f"  expected_end_node and last_node: {bool(expected_end_node and last_node)}")
        if expected_end_node and last_node:
            print(f"  last_node != expected_end_node: {last_node != expected_end_node}")
            print(f"  expected_end_node != 'END': {expected_end_node != 'END'}")
            wrong_branch = expected_end_node and last_node and last_node != expected_end_node and expected_end_node != "END"
            print(f"  WRONG_BRANCH condition: {wrong_branch}")

        # Check the PREMATURE_TERMINATION condition
        print(f"\nChecking PREMATURE_TERMINATION condition:")
        print(f"  last_node: {last_node}")
        print(f"  last_node.upper(): {last_node.upper() if last_node else None}")
        print(f"  last_node and last_node.upper() != 'END': {bool(last_node and last_node.upper() != 'END')}")
        premature_term = last_node and last_node.upper() != "END"
        print(f"  PREMATURE_TERMINATION condition: {premature_term}")

        # Check LOOP_OVERFLOW condition
        print(f"\nChecking LOOP_OVERFLOW condition:")
        from collections import Counter
        counts = Counter(t.get("node_name") for t in trace)
        print(f"  counts: {counts}")
        loop_overflow = False
        for node, count in counts.items():
            if count > max_loops:
                print(f"    Node '{node}': count={count} > max_loops={max_loops}")
                loop_overflow = True
        print(f"  LOOP_OVERFLOW condition: {loop_overflow}")

        # If we got here, check other failure types...
        print(f"\nChecking other failure types (simplified)...")
        print(f"  Would continue to check LOST_IN_MIDDLE, TOOL_HALLUCINATION, etc.")

    # Now call the actual classifier
    print(f"\n--- Actual classifier call ---")
    failure_result = classifier.classify(trace, expected_end_node=expected_end_node, max_loops=max_loops, model_token_limit=model_token_limit)
    print(f"Actual failure result: {failure_result}")
# Debug what the classifier does with our mock trace data

import sys
import os

# Test our mock trace
print("=== OUR MOCK TRACE CLASSIFIER DEBUG ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/05_pr_security_agent'))

# Create our mock trace (the one that's failing)
trace_with_name_keys = [
    {"name": "supervisor"},
    {"name": "security_scan"},
    {"name": "quality_check"},
    {"name": "analytics_eval"}
]

# Convert to the format that has node_name keys (what we think the classifier wants)
trace_with_node_name_keys = []
for node in trace_with_name_keys:
    node_copy = node.copy()
    if "name" in node and "node_name" not in node:
        node_copy["node_name"] = node["name"]
    trace_with_node_name_keys.append(node_copy)

print(f"trace_with_name_keys: {trace_with_name_keys}")
print(f"trace_with_node_name_keys: {trace_with_node_name_keys}")

from langgraph_evals.core.failure_classifier import FailureClassifier
classifier = FailureClassifier()

print(f"\n--- Testing with name keys ---")
failure_result_name = classifier.classify(trace_with_name_keys)
print(f"Failure result with name keys: {failure_result_name}")

print(f"\n--- Testing with node_name keys ---")
failure_result_node_name = classifier.classify(trace_with_node_name_keys)
print(f"Failure result with node_name keys: {failure_result_node_name}")

# Let's also test what happens if we manually add END node to make it complete
print(f"\n--- Testing with END node appended ---")
trace_with_end = trace_with_name_keys + [{"name": "END"}]
trace_with_end_node_name = trace_with_node_name_keys + [{"node_name": "END"}]

print(f"trace_with_end: {trace_with_end}")
failure_result_end_name = classifier.classify(trace_with_end)
print(f"Failure result with END (name keys): {failure_result_end_name}")

print(f"trace_with_end_node_name: {trace_with_end_node_name}")
failure_result_end_node_name = classifier.classify(trace_with_end_node_name)
print(f"Failure result with END (node_name keys): {failure_result_end_node_name}")
# Debug what the assertion function actually receives

import sys
import os

# Test working example to see what gets passed to assert_node_called
print("=== WORKING EXAMPLE ASSERTION INPUT ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent

agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    print("captured_run:", captured_run)
    print("type:", type(captured_run))
    print("keys:", list(captured_run.keys()))
    if 'nodes' in captured_run:
        print("nodes:", captured_run['nodes'])
        print("type of nodes:", type(captured_run['nodes']))
        if len(captured_run['nodes']) > 0:
            print("first node:", captured_run['nodes'][0])
            print("type of first node:", type(captured_run['nodes'][0]))

# Now let's manually test what assert_node_called expects
print("\n=== TESTING ASSERTION FUNCTION DIRECTLY ===")
from langgraph_evals.core.assertions import assert_node_called

# Test with the actual structure from GraphRunCapture
test_trace = {
    "nodes": [
        {"name": "process_input"},
        {"name": "format_output"}
    ]
}

print("Testing assert_node_called with:")
print("test_trace:", test_trace)

try:
    assert_node_called(test_trace, "process_input")
    print("SUCCESS: assert_node_called passed")
except Exception as e:
    print("FAILED:", str(e))

# Test with just the nodes list
print("\nTesting assert_node_called with just nodes list:")
try:
    assert_node_called(test_trace["nodes"], "process_input")
    print("SUCCESS: assert_node_called passed with nodes list")
except Exception as e:
    print("FAILED:", str(e))
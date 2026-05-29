# Test what keys are actually in the nodes from both examples

import sys
import os
from collections import Counter

# Test working example
print("=== WORKING EXAMPLE NODE KEYS ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent

agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    nodes = captured_run["nodes"]
    print(f"Number of nodes: {len(nodes)}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node}")
        print(f"      Type: {type(node)}")
        if isinstance(node, dict):
            print(f"      Keys: {sorted(list(node.keys()))}")
            # Test what .get() returns
            print(f"      .get('name'): {repr(node.get('name'))}")
            print(f"      .get('node_name'): {repr(node.get('node_name'))}")
        print()

# Test our example
print("\n=== OUR EXAMPLE NODE KEYS ===")
# Clear modules
modules_to_remove = [k for k in sys.modules.keys() if k.startswith('examples') or k.startswith('agent') or k.startswith('langgraph_evals')]
for mod in modules_to_remove:
    if mod in sys.modules:
        del sys.modules[mod]

sys.path.insert(0, os.path.join(os.getcwd(), 'examples/05_pr_security_agent'))
from langgraph_evals.langgraph.runner import GraphRunCapture
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

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    nodes = captured_run["nodes"]
    print(f"Number of nodes: {len(nodes)}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node}")
        print(f"      Type: {type(node)}")
        if isinstance(node, dict):
            print(f"      Keys: {sorted(list(node.keys()))}")
            # Test what .get() returns
            print(f"      .get('name'): {repr(node.get('name'))}")
            print(f"      .get('node_name'): {repr(node.get('node_name'))}")
        print()

# Now test what the classifier actually computes
print("\n=== CLASSIFIER COUNTS COMPARISON ===")
print("Working example:")

working_nodes = []  # We'll capture this properly
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent
agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}
with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    working_nodes = captured_run["nodes"]

print(f"  Nodes: {working_nodes}")
node_names_working = [t.get("node_name") for t in working_nodes]
print(f"  t.get('node_name') for each: {node_names_working}")
counts_working = Counter(t.get("node_name") for t in working_nodes)
print(f"  Counter(t.get('node_name')): {counts_working}")

print("\nOur example:")
our_nodes = []
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/05_pr_security_agent'))
from langgraph_evals.langgraph.runner import GraphRunCapture
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
with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    our_nodes = captured_run["nodes"]

print(f"  Nodes: {our_nodes}")
node_names_our = [t.get("node_name") for t in our_nodes]
print(f"  t.get('node_name') for each: {node_names_our}")
counts_our = Counter(t.get("node_name") for t in our_nodes)
print(f"  Counter(t.get('node_name')): {counts_our}")

print("\n=== TESTING WITH 'name' INSTEAD ===")
print("Working example with 'name':")
node_names_working_name = [t.get("name") for t in working_nodes]
print(f"  t.get('name') for each: {node_names_working_name}")
counts_working_name = Counter(t.get("name") for t in working_nodes)
print(f"  Counter(t.get('name')): {counts_working_name}")

print("\nOur example with 'name':")
node_names_our_name = [t.get("name") for t in our_nodes]
print(f"  t.get('name') for each: {node_names_our_name}")
counts_our_name = Counter(t.get("name") for t in our_nodes)
print(f"  Counter(t.get('name')): {counts_our_name}")
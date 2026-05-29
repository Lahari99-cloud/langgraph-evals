# Simple debug to check what the classifier sees

# First, let's check what the working example produces
import sys
import os

# Clear modules to avoid conflicts
modules_to_remove = [k for k in sys.modules.keys() if k.startswith('examples')]
for mod in modules_to_remove:
    del sys.modules[mod]

# Test working example
print("=== WORKING EXAMPLE ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from agent import create_agent as create_working_agent
from langgraph_evals.langgraph.runner import GraphRunCapture

agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    nodes = captured_run["nodes"]
    print(f"Nodes: {nodes}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node} (type: {type(node)})")
        if isinstance(node, dict):
            print(f"      Keys: {list(node.keys())}")
            for k in ['name', 'node_name']:
                if k in node:
                    print(f"      {k}: {node[k]}")

# Now test our example - clear modules again
print("\n=== OUR EXAMPLE ===")
modules_to_remove = [k for k in sys.modules.keys() if k.startswith('examples') or k.startswith('agent')]
for mod in modules_to_remove:
    if mod in sys.modules:
        del sys.modules[mod]

sys.path.insert(0, os.path.join(os.getcwd(), 'examples/05_pr_security_agent'))
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
    print(f"Nodes: {nodes}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node} (type: {type(node)})")
        if isinstance(node, dict):
            print(f"      Keys: {list(node.keys())}")
            for k in ['name', 'node_name']:
                if k in node:
                    print(f"      {k}: {node[k]}")
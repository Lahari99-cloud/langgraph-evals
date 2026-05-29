# Detailed debug to see exactly what's in the nodes

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
    print(f"Number of nodes: {len(nodes)}")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {node}")
        print(f"      Type: {type(node)}")
        if isinstance(node, dict):
            print(f"      Keys: {sorted(list(node.keys()))}")
            for k, v in node.items():
                print(f"        {k}: {repr(v)} (type: {type(v)})")
        print()

# Test our example
print("\n=== OUR EXAMPLE NODES ===")
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
            for k, v in node.items():
                print(f"        {k}: {repr(v)} (type: {type(v)})")
        print()
# Debug the classifier step by step

import sys
import os
from collections import Counter

# Test with working example first
print("=== WORKING EXAMPLE CLASSIFIER TRACE ===")
sys.path.insert(0, os.path.join(os.getcwd(), 'examples/04_langgraph_integration'))
from langgraph_evals.langgraph.runner import GraphRunCapture
from agent import create_agent as create_working_agent

agent = create_working_agent()
initial_state = {"input": "test", "steps": [], "result": None}

with GraphRunCapture(agent, initial_state) as captured_run:
    result = agent.invoke(initial_state)
    trace = captured_run["nodes"]
    print(f"Trace: {trace}")

    # Manual trace of classifier
    print("\n--- Manual Classifier Trace ---")
    print(f"trace: {trace}")

    # Check if trace is empty
    if not trace:
        print("TRACE IS EMPTY")
    else:
        print("TRACE NOT EMPTY")

        # Check last_node = trace[-1].get("node_name")
        last_node = trace[-1].get("node_name")
        print(f"last_node = trace[-1].get('node_name'): {last_node}")
        print(f"  trace[-1]: {trace[-1]}")
        print(f"  trace[-1].get('node_name'): {trace[-1].get('node_name')}")
        print(f"  trace[-1].get('name'): {trace[-1].get('name')}")

        # Check counts = Counter(t.get("node_name") for t in trace)
        node_name_values = [t.get("node_name") for t in trace]
        print(f"t.get('node_name') for each t: {node_name_values}")
        counts = Counter(t.get("node_name") for t in trace)
        print(f"Counter(t.get('node_name') for t in trace): {counts}")

        # Check the loop condition
        max_loops = 3  # default
        print(f"\nChecking loop condition with max_loops={max_loops}")
        for node, count in counts.items():
            print(f"  Node '{node}': count={count}, count > max_loops? {count > max_loops}")
            if count > max_loops:
                print(f"    -> WOULD RETURN LOOP_OVERFLOW")

        # Check premature termination
        expected_end_node = "END"
        if last_node and last_node.upper() != "END":
            print(f"Would return PREMATURE_TERMINATION because last_node='{last_node}' and last_node.upper()='{last_node.upper()}' != 'END'")
        elif last_node is None:
            print(f"last_node is None, so last_node.upper() would fail")
        else:
            print(f"last_node='{last_node}', last_node.upper()='{last_node.upper()}' == 'END', so no PREMATURE_TERMINATION")

print("\n" + "="*50)
print("=== OUR EXAMPLE CLASSIFIER TRACE ===")

# Clear modules
modules_to_remove = [k for k in sys.modules.keys() if k.startswith('examples') or k.startswith('agent') or k.startswith('langgraph_evals')]
for mod in modules_to_remove:
    if mod in sys.modules:
        del sys.modules[mod]

# Test our example
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
    trace = captured_run["nodes"]
    print(f"Trace: {trace}")

    # Manual trace of classifier
    print("\n--- Manual Classifier Trace ---")
    print(f"trace: {trace}")

    # Check if trace is empty
    if not trace:
        print("TRACE IS EMPTY")
    else:
        print("TRACE NOT EMPTY")

        # Check last_node = trace[-1].get("node_name")
        last_node = trace[-1].get("node_name")
        print(f"last_node = trace[-1].get('node_name'): {last_node}")
        print(f"  trace[-1]: {trace[-1]}")
        print(f"  trace[-1].get('node_name'): {trace[-1].get('node_name')}")
        print(f"  trace[-1].get('name'): {trace[-1].get('name')}")

        # Check counts = Counter(t.get("node_name") for t in trace)
        node_name_values = [t.get("node_name") for t in trace]
        print(f"t.get('node_name') for each t: {node_name_values}")
        counts = Counter(t.get("node_name") for t in trace)
        print(f"Counter(t.get('node_name') for t in trace): {counts}")

        # Check the loop condition
        max_loops = 3  # default
        print(f"\nChecking loop condition with max_loops={max_loops}")
        for node, count in counts.items():
            print(f"  Node '{node}': count={count}, count > max_loops? {count > max_loops}")
            if count > max_loops:
                print(f"    -> WOULD RETURN LOOP_OVERFLOW")

        # Check premature termination
        expected_end_node = "END"
        if last_node and last_node.upper() != "END":
            print(f"Would return PREMATURE_TERMINATION because last_node='{last_node}' and last_node.upper()='{last_node.upper()}' != 'END'")
        elif last_node is None:
            print(f"last_node is None, so last_node.upper() would fail")
        else:
            print(f"last_node='{last_node}', last_node.upper()='{last_node.upper()}' == 'END', so no PREMATURE_TERMINATION")
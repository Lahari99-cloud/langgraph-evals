import sys
sys.path.append('examples/05_pr_security_agent')

# Test the monkey patching directly
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class SimpleState(TypedDict):
    steps: List[str]

def node1(state: SimpleState) -> SimpleState:
    return {**state, "steps": state["steps"] + ["node1"]}

def node2(state: SimpleState) -> SimpleState:
    return {**state, "steps": state["steps"] + ["node2"]}

def create_simple_graph() -> StateGraph:
    workflow = StateGraph(SimpleState)
    workflow.add_node("node1", node1)
    workflow.add_node("node2", node2)
    workflow.set_entry_point("node1")
    workflow.add_edge("node1", "node2")
    workflow.add_edge("node2", END)
    return workflow.compile()

# Test GraphRunCapture
from langgraph_evals.langgraph.runner import GraphRunCapture

graph = create_simple_graph()
initial_state = {"steps": []}

print("Testing GraphRunCapture with simple graph...")
with GraphRunCapture(graph, initial_state) as captured_run:
    print("Before invoke - captured_run keys:", list(captured_run.keys()))
    print("Before invoke - nodes:", captured_run.get("nodes", "KEY MISSING"))

    result = graph.invoke({"steps": []})

    print("After invoke - result:", result)
    print("After invoke - captured_run keys:", list(captured_run.keys()))
    print("After invoke - nodes:", captured_run.get("nodes", "KEY MISSING"))
    print("After invoke - final_state:", captured_run.get("final_state"))
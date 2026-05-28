"""
Real LangGraph integration utilities for langgraph-evals.
Provides tools to capture and work with actual LangGraph StateGraph executions.
"""
from contextlib import contextmanager
from typing import Dict, List, Any, Optional, Iterator
import langgraph
from langgraph.graph import StateGraph


@contextmanager
def GraphRunCapture(graph: StateGraph, initial_state: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """
    Context manager that captures a LangGraph execution in the format expected by langgraph-evals assertions.

    Args:
        graph: Compiled LangGraph StateGraph
        initial_state: Initial state to pass to graph.invoke()

    Yields:
        dict: Graph run data in the format expected by assertions:
              {
                "nodes_visited": [{"name": "node1"}, {"name": "node2"}, ...],
                "tool_calls": [...],
                "outputs": {...},
                "final_state": {...}
              }

    Example:
        >>> from langgraph.graph import StateGraph, END
        >>> from typing import TypedDict
        >>>
        >>> class State(TypedDict):
        ...     input: str
        ...     steps: List[str]
        ...
        >>> def node1(state):
        ...     return {**state, "steps": state["steps"] + ["node1"]}
        >>>
        >>> builder = StateGraph(State)
        >>> builder.add_node("node1", node1)
        >>> builder.set_entry_point("node1")
        >>> builder.add_edge("node1", END)
        >>> graph = builder.compile()
        >>>
        >>> with GraphRunCapture(graph, {"input": "test", "steps": []}) as run:
        ...     result = graph.invoke({"input": "test", "steps": []})
        ...     # run now contains the captured execution data
        ...     assert_node_called(run, "node1")
    """
    # We'll monkey-patch the graph's invoke method to capture node visits
    original_invoke = graph.invoke

    captured_data = {
        "nodes_visited": [],
        "tool_calls": [],
        "outputs": {},
        "final_state": None
    }

    def capturing_invoke(*args, **kwargs):
        # Reset captured data for this invocation
        captured_data["nodes"] = []  # This is what assertions expect
        captured_data["tool_calls"] = []
        captured_data["outputs"] = {}

        # Call the original invoke
        result = original_invoke(*args, **kwargs)
        captured_data["final_state"] = result

        # Extract node visits from the result
        # LangGraph StateGraph typically stores execution steps in a 'steps' list in the state
        if isinstance(result, dict) and "steps" in result:
            # Convert steps list to the expected node visit format: [{"name": "step1"}, ...]
            for step in result["steps"]:
                if isinstance(step, str):
                    captured_data["nodes"].append({"name": step})
                elif isinstance(step, dict) and "name" in step:
                    captured_data["nodes"].append(step)

        # Extract outputs (everything except internal state tracking)
        if isinstance(result, dict):
            for key, value in result.items():
                # Skip internal LangGraph state tracking keys
                if key not in ["steps"] and not key.startswith("__"):
                    captured_data["outputs"][key] = value

        return result

    # Patch the invoke method
    graph.invoke = capturing_invoke

    try:
        yield captured_data
    finally:
        # Restore original method
        graph.invoke = original_invoke


def extract_graph_run_data(graph_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured data from a LangGraph invoke result for use with assertions.

    Args:
        graph_result: The raw result from graph.invoke()

    Returns:
        dict: Data in the format expected by langgraph-evals assertions
    """
    # This is a helper for when you don't want to use the context manager
    # but already have a graph result

    extracted = {
        "nodes": [],
        "tool_calls": [],
        "outputs": {},
        "final_state": graph_result
    }

    if isinstance(graph_result, dict):
        # Extract steps if present (LangGraph typically stores execution trail in 'steps')
        if "steps" in graph_result:
            for step in graph_result["steps"]:
                if isinstance(step, str):
                    extracted["nodes"].append({"name": step})
                elif isinstance(step, dict) and "name" in step:
                    extracted["nodes"].append(step)

        # Extract outputs (everything except internal state tracking)
        for key, value in graph_result.items():
            # Skip internal LangGraph state tracking keys
            if key not in ["steps"] and not key.startswith("__"):
                extracted["outputs"][key] = value

    return extracted
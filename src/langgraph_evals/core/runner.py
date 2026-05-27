"""Test runner for LangGraph evaluations."""

from .assertions import (
    assert_node_called,
    assert_node_output,
    assert_node_order,
    assert_no_node_called,
    assert_tool_called,
    assert_tool_not_called
)


def evaluate_graph_run(graph_run):
    """
    Evaluate a LangGraph run and return a Trajectory object.

    Args:
        graph_run: Raw graph run object from LangGraph

    Returns:
        Trajectory: Parsed trajectory for assertions
    """
    # Convert various graph run formats to our Trajectory
    if isinstance(graph_run, Trajectory):
        return graph_run

    # Try to extract nodes and tool_calls from common formats
    nodes = []
    tool_calls = []

    # Handle different possible graph run structures
    if hasattr(graph_run, 'nodes'):
        nodes = graph_run.nodes
    elif isinstance(graph_run, dict) and 'nodes' in graph_run:
        nodes = graph_run['nodes']

    if hasattr(graph_run, 'tool_calls'):
        tool_calls = graph_run.tool_calls
    elif isinstance(graph_run, dict) and 'tool_calls' in graph_run:
        tool_calls = graph_run['tool_calls']

    return Trajectory(nodes=nodes, tool_calls=tool_calls)


# Export assertion functions for ease of use
__all__ = [
    'evaluate_graph_run',
    'assert_node_called',
    'assert_node_output',
    'assert_node_order',
    'assert_no_node_called',
    'assert_tool_called',
    'assert_tool_not_called'
]
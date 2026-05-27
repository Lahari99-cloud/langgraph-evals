"""Example test demonstrating the langgraph-evals pytest plugin."""

from langgraph_evals.core.runner import (
    assert_node_called,
    assert_node_output,
    assert_node_order,
    assert_no_node_called,
    assert_tool_called,
    assert_tool_not_called
)


def test_langgraph_evaluations_work(trajectory_fixture):
    """Example test showing how to use the assertions."""
    # This would normally come from evaluating a LangGraph run
    trajectory = trajectory_fixture

    # Example assertions
    assert_node_called(trajectory, "start_node")
    assert_node_output(trajectory, "processor", "result", "success")
    assert_node_order(trajectory, ["start_node", "processor", "end_node"])
    assert_no_node_called(trajectory, "failed_node")
    assert_tool_called(trajectory, "search_tool")
    assert_tool_not_called(trajectory, "delete_tool")


# Example fixture for demonstration
import pytest

@pytest.fixture
def trajectory_fixture():
    """Provide a sample trajectory for testing."""
    # Create a mock trajectory-like object for the assertions
    class MockTrajectory:
        def __init__(self, nodes, tool_calls):
            self.nodes = nodes
            self.tool_calls = tool_calls

    return MockTrajectory(
        nodes=[
            {"name": "start_node", "output": {"step": 1}},
            {"name": "processor", "output": {"result": "success", "step": 2}},
            {"name": "end_node", "output": {"step": 3}}
        ],
        tool_calls=[
            {"name": "search_tool", "args": {"query": "test"}},
            {"name": "fetch_tool", "args": {"url": "http://example.com"}}
        ]
    )
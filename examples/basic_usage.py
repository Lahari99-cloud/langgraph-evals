"""
Basic usage example for langgraph-evals.
This demonstrates how to use the assertions in tests.
"""

import pytest
from langgraph_evals.core.trajectory import Trajectory
from langgraph_evals.core.runner import (
    assert_node_called,
    assert_node_output,
    assert_node_order,
    assert_no_node_called,
    assert_tool_called,
    assert_tool_not_called
)


def test_basic_assertions():
    """Test basic assertions functionality."""
    # Create a sample trajectory (this would come from evaluating a LangGraph run)
    trajectory = Trajectory(
        nodes=[
            {"name": "initialize", "output": {"status": "ready"}},
            {"name": "fetch_data", "output": {"count": 10, "source": "api"}},
            {"name": "process_data", "output": {"result": "success", "processed": 10}},
            {"name": "save_results", "output": {"saved": True}}
        ],
        tool_calls=[
            {"name": "http_request", "args": {"url": "https://api.example.com/data"}},
            {"name": "database_query", "args": {"table": "results", "operation": "INSERT"}}
        ]
    )

    # Test assertions - all should pass
    assert_node_called(trajectory, "fetch_data")
    assert_node_output(trajectory, "fetch_data", "count", 10)
    assert_node_output(trajectory, "process_data", "result", "success")
    assert_node_order(trajectory, ["initialize", "fetch_data", "process_data", "save_results"])
    assert_no_node_called(trajectory, "error_handler")
    assert_tool_called(trajectory, "http_request")
    assert_tool_not_called(trajectory, "delete_tool")


def test_assertion_failures():
    """Test that assertions fail with helpful messages."""
    trajectory = Trajectory(
        nodes=[
            {"name": "node_a", "output": {"value": 1}},
            {"name": "node_b", "output": {"value": 2}}
        ],
        tool_calls=[
            {"name": "tool_x", "args": {}}
        ]
    )

    # Test failing assertions
    with pytest.raises(AssertionError, match="Expected node 'nonexistent' to be called"):
        assert_node_called(trajectory, "nonexistent")

    with pytest.raises(AssertionError, match="Expected: 999"):
        assert_node_output(trajectory, "node_a", "value", 999)

    with pytest.raises(AssertionError, match="Expected: \\['node_a', 'nonexistent', 'node_b'\\]"):
        assert_node_order(trajectory, ["node_a", "nonexistent", "node_b"])

    with pytest.raises(AssertionError, match="Expected node 'node_a' to NOT be called"):
        assert_no_node_called(trajectory, "node_a")

    with pytest.raises(AssertionError, match="Expected tool 'nonexistent' to be called"):
        assert_tool_called(trajectory, "nonexistent")

    with pytest.raises(AssertionError, match="Expected tool 'tool_x' to NOT be called"):
        assert_tool_not_called(trajectory, "tool_x")


if __name__ == "__main__":
    # Run the tests
    test_basic_assertions()
    test_assertion_failures()
    print("All tests passed!")
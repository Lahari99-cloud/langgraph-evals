"""Tests for the assertions module."""

import pytest
from langgraph_evals.core.assertions import (
    assert_node_called,
    assert_node_output,
    assert_node_order,
    assert_no_node_called,
    assert_tool_called,
    assert_tool_not_called
)


def test_assert_node_called():
    """Test asserting that a node was called."""
    # Create a mock trajectory-like object for assertions
    class MockTrajectory:
        def __init__(self, nodes):
            self.nodes = nodes

    trajectory = MockTrajectory(
        nodes=[
            {"name": "node_a", "output": {"result": "success"}},
            {"name": "node_b", "output": {"result": "failure"}}
        ]
    )

    # Should pass
    assert_node_called(trajectory, "node_a")
    assert_node_called(trajectory, "node_b")

    # Should fail
    with pytest.raises(AssertionError, match="Expected node 'node_c' to be called"):
        assert_node_called(trajectory, "node_c")


def test_assert_node_output():
    """Test asserting node output values."""
    # Create a mock trajectory-like object for assertions
    class MockTrajectory:
        def __init__(self, nodes):
            self.nodes = nodes

    trajectory = MockTrajectory(
        nodes=[
            {"name": "processor", "output": {"status": "ok", "count": 5}},
            {"name": "finalizer", "output": {"status": "done"}}
        ]
    )

    # Should pass
    assert_node_output(trajectory, "processor", "status", "ok")
    assert_node_output(trajectory, "processor", "count", 5)
    assert_node_output(trajectory, "finalizer", "status", "done")

    # Should fail - wrong value
    with pytest.raises(AssertionError, match="Expected: 'error'"):
        assert_node_output(trajectory, "processor", "status", "error")

    # Should fail - node not called
    with pytest.raises(AssertionError, match="Expected node 'missing' to be called"):
        assert_node_output(trajectory, "missing", "any_key", "any_value")


def test_assert_node_order():
    """Test asserting node call order."""
    # Create a mock trajectory-like object for assertions
    class MockTrajectory:
        def __init__(self, nodes):
            self.nodes = nodes

    trajectory = MockTrajectory(
        nodes=[
            {"name": "start", "output": {}},
            {"name": "process", "output": {}},
            {"name": "end", "output": {}}
        ]
    )

    # Should pass
    assert_node_order(trajectory, ["start", "process", "end"])

    # Should fail - wrong order
    with pytest.raises(AssertionError, match="Expected: \\['start', 'end', 'process'\\]"):
        assert_node_order(trajectory, ["start", "end", "process"])

    # Should fail - missing node
    with pytest.raises(AssertionError, match="Expected: \\['start', 'missing', 'end'\\]"):
        assert_node_order(trajectory, ["start", "missing", "end"])


def test_assert_no_node_called():
    """Test asserting that a node was NOT called."""
    # Create a mock trajectory-like object for assertions
    class MockTrajectory:
        def __init__(self, nodes):
            self.nodes = nodes

    trajectory = MockTrajectory(
        nodes=[
            {"name": "node_a", "output": {}},
            {"name": "node_b", "output": {}}
        ]
    )

    # Should pass
    assert_no_node_called(trajectory, "node_c")
    assert_no_node_called(trajectory, "node_d")

    # Should fail
    with pytest.raises(AssertionError, match="Expected node 'node_a' to NOT be called"):
        assert_no_node_called(trajectory, "node_a")


def test_assert_tool_called():
    """Test asserting that a tool was called."""
    # Create a mock trajectory-like object for assertions
    class MockTrajectory:
        def __init__(self, tool_calls=None):
            self.nodes = []  # Default empty nodes
            self.tool_calls = tool_calls or []

    trajectory = MockTrajectory(
        tool_calls=[
            {"name": "search_tool", "args": {"query": "test"}},
            {"name": "calculate_tool", "args": {"x": 1, "y": 2}}
        ]
    )

    # Should pass
    assert_tool_called(trajectory, "search_tool")
    assert_tool_called(trajectory, "calculate_tool")

    # Should fail
    with pytest.raises(AssertionError, match="Expected tool 'missing_tool' to be called"):
        assert_tool_called(trajectory, "missing_tool")


def test_assert_tool_not_called():
    """Test asserting that a tool was NOT called."""
    # Create a mock trajectory-like object for assertions
    class MockTrajectory:
        def __init__(self, tool_calls=None):
            self.nodes = []  # Default empty nodes
            self.tool_calls = tool_calls or []

    trajectory = MockTrajectory(
        tool_calls=[
            {"name": "search_tool", "args": {}},
            {"name": "fetch_tool", "args": {}}
        ]
    )

    # Should pass
    assert_tool_not_called(trajectory, "calculate_tool")
    assert_tool_not_called(trajectory, "missing_tool")

    # Should fail
    with pytest.raises(AssertionError, match="Expected tool 'search_tool' to NOT be called"):
        assert_tool_not_called(trajectory, "search_tool")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
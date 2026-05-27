"""
Test for the simple LangGraph agent example.
Demonstrates usage of langgraph-evals assertion utilities and TrajectoryScorer.
"""

import pytest
from langgraph_evals.core.assertions import (
    assert_node_called,
    assert_node_order,
    assert_tool_called
)
from langgraph_evals.core.trajectory import TrajectoryScorer
from agent import create_simple_agent


def test_simple_agent_assertions():
    """Test that the simple agent works with langgraph-evals assertions."""
    # Create the agent
    agent = create_simple_agent()

    # Invoke the agent
    initial_state = {
        "input": "test input",
        "steps": [],
        "result": None
    }

    result = agent.invoke(initial_state)

    # Extract trace information for assertions
    # In a real scenario, this would come from LangGraph's tracing
    # For this example, we'll simulate the trace
    trace = {
        "nodes": [
            {"name": "process_input"},
            {"name": "format_output"}
        ]
    }

    # Test assertions
    assert_node_called(trace, "process_input")
    assert_node_called(trace, "format_output")
    assert_node_order(trace, ["process_input", "format_output"])

    # Test that a non-existent node was not called
    from langgraph_evals.core.assertions import assert_no_node_called
    assert_no_node_called(trace, "nonexistent_node")

    # Test TrajectoryScorer
    scorer = TrajectoryScorer()
    node_sequence = ["process_input", "format_output"]
    report = scorer.score(node_sequence, expected_end_node="format_output")

    assert report.completion_score == 1.0
    assert report.efficiency_score == 1.0  # No repeated nodes
    assert report.loops_detected == []  # No loops detected (returns list, not int)
    assert report.dead_end_detected == False

    # Verify the actual result
    assert "RESULT: Processed: test input" in result["result"]
    assert result["steps"] == ["process_input", "format_output"]


def test_simple_agent_with_different_input():
    """Test the agent with different input to ensure it works generally."""
    agent = create_simple_agent()

    test_cases = [
        "first test",
        "second test with more words",
        "123 numbers",
        ""  # empty string
    ]

    for test_input in test_cases:
        initial_state = {
            "input": test_input,
            "steps": [],
            "result": None
        }

        result = agent.invoke(initial_state)
        expected_result = f"RESULT: Processed: {test_input}"
        assert result["result"] == expected_result
        assert result["steps"] == ["process_input", "format_output"]
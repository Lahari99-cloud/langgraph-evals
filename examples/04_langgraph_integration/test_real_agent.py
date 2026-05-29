"""
Test demonstrating real LangGraph integration with langgraph-evals assertions.
This shows how to use GraphRunCapture to work with actual StateGraph executions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from langgraph_evals.langgraph.runner import GraphRunCapture
from langgraph_evals.core.assertions import (
    assert_node_called,
    assert_node_order,
    assert_no_node_called,
    assert_tool_called,
    assert_tool_not_called
)
from langgraph_evals.core.trajectory import TrajectoryScorer
from langgraph_evals.core.failure_classifier import FailureClassifier
from agent import create_agent


def test_real_langgraph_with_assertions():
    """Test that langgraph-evals assertions work with real LangGraph executions."""
    # Create the agent
    agent = create_agent()

    # Use GraphRunCapture to capture the execution
    with GraphRunCapture(agent, {"input": "test", "steps": [], "result": None}) as captured_run:
        # Invoke the agent - execution is captured automatically
        result = agent.invoke({"input": "hello world", "steps": [], "result": None})

        # Verify the result is correct
        assert result["result"] == "RESULT: Processed: hello world"
        assert result["steps"] == ["process_input", "format_output"]

        # Now apply langgraph-evals assertions to the captured data
        assert_node_called(captured_run, "process_input")
        assert_node_called(captured_run, "format_output")
        assert_node_order(captured_run, ["process_input", "format_output"])
        assert_no_node_called(captured_run, "nonexistent_node")


def test_real_langgraph_with_trajectory_scoring():
    """Test that TrajectoryScorer works with real LangGraph executions."""
    agent = create_agent()

    with GraphRunCapture(agent, {"input": "test", "steps": [], "result": None}) as captured_run:
        result = agent.invoke({"input": "test data", "steps": [], "result": None})

        # Extract the node sequence for scoring
        node_sequence = [node["name"] for node in captured_run["nodes"]]
        # Expected: ["process_input", "format_output"]

        scorer = TrajectoryScorer()
        report = scorer.score(node_sequence, expected_end_node="format_output")

        assert report.completion_score == 1.0
        assert report.efficiency_score == 1.0  # No repeated nodes
        assert report.loops_detected == []  # No loops
        assert report.dead_end_detected == False


def test_real_langgraph_with_failure_classification():
    """Test that FailureClassifier works with real LangGraph executions."""
    agent = create_agent()

    # Test normal execution (should not detect failures)
    with GraphRunCapture(agent, {"input": "normal", "steps": [], "result": None}) as captured_run:
        result = agent.invoke({"input": "test", "steps": [], "result": None})

        classifier = FailureClassifier()
        failure_result = classifier.classify(captured_run["nodes"])

        # Normal execution should not trigger any failures
        assert failure_result is None

    # To test failure detection, we'd need to create a graph that actually fails
    # This demonstrates the mechanism works with real graph data


def test_extract_helper_function():
    """Test the extract_graph_run_data helper function."""
    from langgraph_evals.langgraph.runner import extract_graph_run_data

    agent = create_agent()
    result = agent.invoke({"input": "extract test", "steps": [], "result": None})

    # Extract data in the format expected by assertions
    extracted = extract_graph_run_data(result)

    # Verify structure and use assertions
    assert "nodes" in extracted
    assert len(extracted["nodes"]) == 2
    assert extracted["nodes"][0]["name"] == "process_input"
    assert extracted["nodes"][1]["name"] == "format_output"

    # Verify assertions work on extracted data
    assert_node_called(extracted, "process_input")
    assert_node_order(extracted, ["process_input", "format_output"])


if __name__ == "__main__":
    # Run the tests manually
    test_real_langgraph_with_assertions()
    test_real_langgraph_with_trajectory_scoring()
    test_real_langgraph_with_failure_classification()
    test_extract_helper_function()
    print("All real LangGraph integration tests passed!")
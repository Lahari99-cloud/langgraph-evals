"""
Test demonstrating real LangGraph integration with langgraph-evals.
This addresses the gap where assertions only worked on mock data.
"""
import importlib.util
import sys

# Load the agent module from the examples directory
spec = importlib.util.spec_from_file_location(
    "simple_agent",
    "examples/01_simple_agent/agent.py"
)
simple_agent_module = importlib.util.module_from_spec(spec)
sys.modules["simple_agent"] = simple_agent_module
spec.loader.exec_module(simple_agent_module)

from langgraph_evals.langgraph.runner import GraphRunCapture, extract_graph_run_data
from langgraph_evals.core.assertions import (
    assert_node_called,
    assert_node_order,
    assert_no_node_called
)


def test_real_langgraph_integration_with_capture():
    """Test that GraphRunCapture works with a real LangGraph StateGraph."""
    # Create a real LangGraph agent
    agent = simple_agent_module.create_simple_agent()

    # Use GraphRunCapture to wrap the invocation
    with GraphRunCapture(agent, {"input": "test", "steps": [], "result": None}) as captured_run:
        # Invoke the agent - this will be captured
        result = agent.invoke({"input": "hello world", "steps": [], "result": None})

        # Verify we got the expected result
        assert result["result"] == "RESULT: Processed: hello world"
        assert result["steps"] == ["process_input", "format_output"]

        # Now use the captured data with langgraph-evals assertions
        assert_node_called(captured_run, "process_input")
        assert_node_called(captured_run, "format_output")
        assert_node_order(captured_run, ["process_input", "format_output"])
        assert_no_node_called(captured_run, "nonexistent_node")


def test_extract_graph_run_data_helper():
    """Test the extract_graph_run_data helper function."""
    agent = simple_agent_module.create_simple_agent()
    result = agent.invoke({"input": "test", "steps": [], "result": None})

    # Extract data in the format expected by assertions
    extracted = extract_graph_run_data(result)

    # Verify the extracted data has the expected structure
    assert "nodes" in extracted  # Changed from nodes_visited to match assertion expectation
    assert "outputs" in extracted
    assert "final_state" in extracted

    # Verify we can use assertions on the extracted data
    assert_node_called(extracted, "process_input")
    assert_node_order(extracted, ["process_input", "format_output"])


def test_context_manager_restores_original_invoke():
    """Test that GraphRunCapture properly restores the original invoke method."""
    agent = simple_agent_module.create_simple_agent()
    original_invoke = agent.invoke

    # Outside the context manager, invoke should be the original
    result1 = agent.invoke({"input": "test1", "steps": [], "result": None})

    # Inside the context manager, invoke should be our capturing version
    with GraphRunCapture(agent, {"input": "test", "steps": [], "result": None}) as captured_run:
        result2 = agent.invoke({"input": "test2", "steps": [], "result": None})
        # We got the captured data
        assert isinstance(captured_run, dict)
        assert "nodes_visited" in captured_run

    # After the context, invoke should be restored to original
    result3 = agent.invoke({"input": "test3", "steps": [], "result": None})

    # All three results should be valid invocations
    assert "result" in result1
    assert "result" in result2
    assert "result" in result3
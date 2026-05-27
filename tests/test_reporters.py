"""Tests for LangGraph evaluation reporters."""
import json
import os
import tempfile
from langgraph_evals.reporters.console import ConsoleReporter
from langgraph_evals.reporters.json import JsonReporter


def test_console_reporter_runs_without_error():
    """Test that ConsoleReporter.report() runs without error on valid input."""
    reporter = ConsoleReporter()

    # Valid input data
    results = {
        "timestamp": "2026-05-27T10:00:00Z",
        "graph": "test_graph",
        "assertions": {
            "assert_node_called": True,
            "assert_node_output": False,
            "assert_node_order": True
        },
        "trajectory": {
            "efficiency_score": 0.85,
            "completion_score": 1.0,
            "loops_detected": 0,
            "dead_end_detected": False
        },
        "failures": {
            "LOOP_OVERFLOW": {
                "name": "LOOP_OVERFLOW",
                "description": "any node appears more than max_loops times",
                "evidence": "Node execution counts: {'process': 5}",
                "remediation": "Add loop detection and termination conditions"
            }
        },
        "summary": {
            "total": 3,
            "passed": 2,
            "failed": 1,
            "success_rate": 0.67
        }
    }

    # This should not raise any exception
    try:
        reporter.report(results)
        assert True  # If we get here, no exception was raised
    except Exception as e:
        assert False, f"ConsoleReporter.report() raised an exception: {e}"


def test_json_reporter_creates_valid_json_file():
    """Test that JsonReporter.report() creates a valid JSON file."""
    reporter = JsonReporter()

    results = {
        "timestamp": "2026-05-27T10:00:00Z",
        "graph": "test_graph",
        "assertions": {
            "assert_node_called": True
        },
        "trajectory": {},
        "failures": {},
        "summary": {
            "total": 1,
            "passed": 1,
            "failed": 0,
            "success_rate": 1.0
        }
    }

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        # Generate the report
        report_data = reporter.report(results, temp_path)

        # Verify the file was created
        assert os.path.exists(temp_path), "JSON report file was not created"

        # Verify the file contains valid JSON
        with open(temp_path, 'r') as f:
            loaded_data = json.load(f)

        # Verify it's the same data that was returned
        assert loaded_data == report_data, "Loaded JSON data does not match returned data"

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_json_file_contains_required_keys():
    """Test that JSON file contains required keys: graph, timestamp, summary."""
    reporter = JsonReporter()

    results = {
        "timestamp": "2026-05-27T10:00:00Z",
        "graph": "test_graph",
        "assertions": {},
        "trajectory": {},
        "failures": {},
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "success_rate": 0.0
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        reporter.report(results, temp_path)

        # Load and verify the JSON
        with open(temp_path, 'r') as f:
            data = json.load(f)

        # Check required keys exist
        assert "graph" in data, "Missing 'graph' key in JSON report"
        assert "timestamp" in data, "Missing 'timestamp' key in JSON report"
        assert "summary" in data, "Missing 'summary' key in JSON report"

        # Check values are correct
        assert data["graph"] == "test_graph"
        assert data["timestamp"] == "2026-05-27T10:00:00Z"
        assert isinstance(data["summary"], dict)

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_console_reporter_handles_empty_results():
    """Test that ConsoleReporter handles empty results dict without crashing."""
    reporter = ConsoleReporter()

    # Empty results
    results = {}

    # This should not raise any exception
    try:
        reporter.report(results)
        assert True  # If we get here, no exception was raised
    except Exception as e:
        assert False, f"ConsoleReporter.report() raised an exception with empty results: {e}"

    # Also test with None values
    results_none = {
        "assertions": None,
        "trajectory": None,
        "failures": None,
        "summary": None
    }

    try:
        reporter.report(results_none)
        assert True  # If we get here, no exception was raised
    except Exception as e:
        assert False, f"ConsoleReporter.report() raised an exception with None values: {e}"
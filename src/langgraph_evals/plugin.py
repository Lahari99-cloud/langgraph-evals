"""Pytest plugin for LangGraph evaluations."""
import json
import pytest

# Module-level plugin declaration
pytest_plugin = True


def pytest_configure(config):
    """Configure the LangGraph evaluations plugin."""
    # Register the lge marker
    config.addinivalue_line(
        "markers", "lge: mark test as a LangGraph evaluation test"
    )


def pytest_addoption(parser):
    """Add custom command line options."""
    group = parser.getgroup("langgraph-evals", "LangGraph Evaluations")
    group.addoption(
        "--lge-report",
        action="store",
        dest="lge_report",
        metavar="FILE",
        default=None,
        help="Output LangGraph evaluation report to FILE in JSON format",
    )
    group.addoption(
        "--lge-verbose",
        action="store_true",
        dest="lge_verbose",
        default=False,
        help="Print verbose node trace during test execution",
    )


@pytest.fixture
def lge_runner():
    """Fixture that returns a configured LangGraph test runner."""
    from langgraph_evals.core.runner import GraphRunner
    return GraphRunner()


def pytest_runtest_makereport(item, call):
    """Handle test execution to collect LangGraph-specific data."""
    if "lge" in item.keywords:
        # This is an LGE test, collect execution data
        if call.when == "call":
            # Store trace data on the item for later use
            if not hasattr(item, "_lge_trace"):
                item._lge_trace = []

            # In a real implementation, we would collect actual trace data
            # For now, we'll simulate some basic trace information
            trace_entry = {
                "node": "test_execution",
                "phase": call.when,
                "duration": getattr(call, "duration", 0),
                "outcome": call.excinfo is None
            }
            item._lge_trace.append(trace_entry)


def pytest_sessionfinish(session, exitstatus):
    """Handle session completion to generate reports."""
    config = session.config
    if getattr(config.option, "lge_report", None):
        # Collect LGE test data and generate report
        lge_data = {
            "session_info": {
                "total_tests": session.testscollected,
                "failed_tests": session.testsfailed,
                "exitstatus": exitstatus
            },
            "lge_tests": []
        }

        # In a real implementation, we would iterate through all test items
        # and collect their trace data. For now, we'll create a placeholder.
        lge_data["lge_tests"].append({
            "test_name": "placeholder",
            "trace": [{"message": "LGE test execution completed"}],
            "status": "passed" if exitstatus == 0 else "failed"
        })

        # Write the report to the specified file
        try:
            with open(config.option.lge_report, "w") as f:
                json.dump(lge_data, f, indent=2)
        except Exception as e:
            # If we can't write the file, we at least don't want to crash pytest
            if config.getvalue("verbose"):
                print(f"Warning: Could not write LGE report: {e}")
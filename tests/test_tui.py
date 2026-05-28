"""
Tests for the TUI Trajectory Tracer.
"""
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from langgraph_evals.tui.tracer import TrajectoryTracer
from langgraph_evals.core.failure_classifier import FailureResult


def test_tracer_display_runs():
    """Test that TrajectoryTracer.display() runs without error on valid input."""
    tracer = TrajectoryTracer()
    # This should not raise
    tracer.display(
        node_sequence=["start", "process", "end"],
        scores={"efficiency": 1.0, "completion": 1.0}
    )


def test_tracer_handles_empty_sequence():
    """Test that TrajectoryTracer.display() handles empty node sequence."""
    tracer = TrajectoryTracer()
    # This should not raise
    tracer.display(
        node_sequence=[],
        scores={"efficiency": 0.0, "completion": 0.0}
    )


def test_cli_demo_runs():
    """Test that CLI demo command runs without error."""
    # Import and run the main function
    from langgraph_evals.tui.cli import main

    # Capture stdout to avoid cluttering test output
    with patch('sys.stdout') as mock_stdout:
        result = main()
        # Should return 0 for success
        assert result == 0
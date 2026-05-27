"""Tests for failure classification functionality."""

import pytest
from langgraph_evals.core.failure_classifier import FailureClassifier, FailureResult


class TestFailureClassifier:
    """Test suite for FailureClassifier."""

    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = FailureClassifier()

    def test_lost_in_middle_detection(self):
        """Test detection of LOST_IN_MIDDLE failure."""
        trace = [
            {
                "node_name": "process",
                "state": "The user asked about quantum computing applications in cryptography. Key points: Shor's algorithm, quantum entanglement, post-quantum cryptography.",
                "output": "I'll help you with that."
            }
        ]

        result = self.classifier.classify(trace)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "LOST_IN_MIDDLE"
        assert result.description == "context in state but not referenced in output"
        assert "State length:" in result.evidence
        assert "Improve output generation" in result.remediation

    def test_tool_hallucination_detection(self):
        """Test detection of TOOL_HALLUCINATION failure."""
        trace = [
            {
                "node_name": "agent",
                "input": "What is the weather in New York?",
                "tool_calls": [
                    {
                        "name": "search_weather",
                        "arguments": {"location": "New York", "date": "tomorrow"},
                        "parameters": {"units": "fahrenheit"}  # This parameter wasn't in input
                    }
                ]
            }
        ]

        result = self.classifier.classify(trace)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "TOOL_HALLUCINATION"
        assert result.description == "tool calls contain parameters not in input"
        assert "Tool call parameters:" in result.evidence
        assert "Validate tool parameters" in result.remediation

    def test_context_overflow_detection(self):
        """Test detection of CONTEXT_OVERFLOW failure."""
        # Create a long input that exceeds 80% of 4096 token limit
        long_input = "A" * (int(4096 * 0.8 * 4) + 100)  # Over 80% limit

        trace = [
            {
                "node_name": "process",
                "input": long_input
            }
        ]

        result = self.classifier.classify(trace, model_token_limit=4096)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "CONTEXT_OVERFLOW"
        assert result.description == "input token count exceeds 80% of model limit"
        assert "Input length:" in result.evidence
        assert "Truncate or summarize input" in result.remediation

    def test_wrong_branch_detection(self):
        """Test detection of WRONG_BRANCH failure."""
        trace = [
            {"node_name": "start"},
            {"node_name": "process"},
            {"node_name": "error_handler"}  # Ended here instead of expected end
        ]

        result = self.classifier.classify(trace, expected_end_node="end_node")

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "WRONG_BRANCH"
        assert result.description == "actual end node differs from expected end node"
        assert "Actual end node:" in result.evidence
        assert "Review graph routing logic" in result.remediation

    def test_memory_bleed_detection(self):
        """Test detection of MEMORY_BLEED failure."""
        trace = [
            {
                "node_name": "node1",
                "thread_id": "thread_1",
                "state": {"user_preference": "dark_mode"}
            },
            {
                "node_name": "node2",
                "thread_id": "thread_2",  # Different thread - this indicates bleed
                "state": {"user_preference": "light_mode"}
            }
        ]

        result = self.classifier.classify(trace)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "MEMORY_BLEED"
        assert result.description == "state contains keys from a different thread_id"
        assert "Thread IDs found:" in result.evidence
        assert "Ensure proper thread isolation" in result.remediation

    def test_loop_overflow_detection(self):
        """Test detection of LOOP_OVERFLOW failure."""
        trace = [
            {"node_name": "process"},
            {"node_name": "process"},
            {"node_name": "process"},
            {"node_name": "process"}  # 4 times, exceeding default max_loops=3
        ]

        result = self.classifier.classify(trace, max_loops=3)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "LOOP_OVERFLOW"
        assert result.description == "any node appears more than max_loops times"
        assert "Node execution counts:" in result.evidence
        assert "Add loop detection and termination conditions" in result.remediation

    def test_premature_termination_detection(self):
        """Test detection of PREMATURE_TERMINATION failure."""
        trace = [
            {"node_name": "start"},
            {"node_name": "process"},
            {"node_name": "middle_node"}  # Never reached END
        ]

        result = self.classifier.classify(trace)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "PREMATURE_TERMINATION"
        assert result.description == "END node never reached"
        assert "Last node executed:" in result.evidence
        assert "Ensure graph has proper termination conditions" in result.remediation

    def test_no_failure_detected(self):
        """Test that normal traces return None (no failure)."""
        trace = [
            {"node_name": "start"},
            {"node_name": "process"},
            {"node_name": "end"}  # Proper termination
        ]

        result = self.classifier.classify(trace, expected_end_node="end")

        assert result is None

    def test_empty_trace(self):
        """Test handling of empty trace."""
        trace = []

        result = self.classifier.classify(trace)

        assert result is not None
        assert isinstance(result, FailureResult)
        assert result.name == "PREMATURE_TERMINATION"
        assert result.description == "END node never reached"
        assert "No trace entries found" in result.evidence
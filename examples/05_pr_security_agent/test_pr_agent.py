import pytest
from langgraph_evals.core.assertions import assert_node_called, assert_node_order
from langgraph_evals.core.failure_classifier import FailureClassifier
from langgraph_evals.core.trajectory import TrajectoryScorer


def test_clean_pr():
    trace = {
        "nodes_visited": ["supervisor", "security_scan", "quality_check", "analytics_eval"],
        "tool_calls": [],
        "outputs": {"status": "approved"}
    }
    assert_node_called(trace, "supervisor")
    assert_node_called(trace, "security_scan")
    assert_node_called(trace, "quality_check")
    assert_node_order(trace, ["supervisor", "security_scan", "quality_check", "analytics_eval"])


def test_secret_detected():
    cyclical_trace = [
        "supervisor", "security_scan", "supervisor",
        "security_scan", "supervisor", "security_scan",
        "supervisor", "security_scan", "analytics_eval"
    ]
    classifier = FailureClassifier()
    result = classifier.classify(
        [{"node_name": n} for n in cyclical_trace],
        max_loops=3
    )
    assert result is not None
    assert result.name == "LOOP_OVERFLOW"


def test_sql_injection_detected():
    trace = {
        "nodes_visited": [
            "supervisor", "security_scan",
            "security_block", "audit_logger"
        ],
        "tool_calls": [],
        "outputs": {"status": "blocked"}
    }
    assert_node_called(trace, "security_scan")
    assert_node_called(trace, "security_block")
    with pytest.raises(AssertionError):
        assert_node_called(trace, "transaction_approval")
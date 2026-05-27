"""Tests for the TrajectoryScorer."""

import pytest
from langgraph_evals.core.trajectory import TrajectoryScorer, TrajectoryReport


def test_trajectory_scorer_basic():
    """Test basic trajectory scoring."""
    scorer = TrajectoryScorer()

    # Simple linear trajectory
    node_sequence = ['start', 'process', 'end']

    report = scorer.score(node_sequence, expected_end_node='end')

    assert isinstance(report, TrajectoryReport)
    assert report.efficiency_score == 1.0  # No wasted steps
    assert report.completion_score == 1.0  # Reached expected end
    assert report.loops_detected == []     # No loops
    assert report.dead_end_detected == False
    assert report.expected_end_node == 'end'
    assert report.actual_end_node == 'end'
    assert len(report.node_visits) == 3
    assert "Successfully reached expected end node" in report.explanation


def test_trajectory_scorer_with_loops():
    """Test scoring with loops."""
    scorer = TrajectoryScorer()

    node_sequence = ['start', 'process', 'process', 'end']  # process visited twice

    report = scorer.score(node_sequence, expected_end_node='end', max_loops=1)  # Consider 2+ visits as loop

    assert report.efficiency_score < 1.0  # Some wasted steps due to loop
    assert report.completion_score == 1.0  # Still reached expected end
    assert 'process' in report.loops_detected  # Process node looped
    assert report.dead_end_detected == False


def test_trajectory_scorer_dead_end():
    """Test scoring when trajectory ends at wrong node."""
    scorer = TrajectoryScorer()

    node_sequence = ['start', 'process', 'wrong_end']  # Ended here instead of expected

    report = scorer.score(node_sequence, expected_end_node='correct_end')

    assert report.efficiency_score > 0.0  # Some efficiency
    assert report.completion_score == 0.0  # Didn't reach expected end
    assert report.dead_end_detected == True
    assert report.expected_end_node == 'correct_end'
    assert report.actual_end_node == 'wrong_end'
    assert "Did not reach expected end node" in report.explanation


def test_trajectory_scorer_no_expectation():
    """Test scoring with no expected end node."""
    scorer = TrajectoryScorer()

    node_sequence = ['start', 'middle', 'end']

    report = scorer.score(node_sequence)  # No expected_end_node

    assert report.completion_score == 1.0  # Default to success when no expectation
    assert report.expected_end_node is None
    assert report.actual_end_node == 'end'


def test_trajectory_scorer_empty_trajectory():
    """Test scoring with empty trajectory."""
    scorer = TrajectoryScorer()

    node_sequence = []

    report = scorer.score(node_sequence, expected_end_node='end')

    assert report.efficiency_score == 0.0
    assert report.completion_score == 0.0  # Failed to reach expected end
    assert report.dead_end_detected == True
    assert report.expected_end_node == 'end'
    assert report.actual_end_node is None
    assert len(report.node_visits) == 0


def test_trajectory_scorer_complex_loop():
    """Test scoring with multiple loops."""
    scorer = TrajectoryScorer()

    node_sequence = ['start', 'A', 'B', 'A', 'B', 'A', 'end']  # A: 3x, B: 2x

    report = scorer.score(node_sequence, expected_end_node='end', max_loops=1)  # Consider 2+ visits as loop

    assert 'A' in report.loops_detected
    assert 'B' in report.loops_detected
    assert report.efficiency_score < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
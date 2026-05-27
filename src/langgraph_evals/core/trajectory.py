from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class NodeVisit:
    node_name: str
    visit_count: int
    order: int

@dataclass
class TrajectoryReport:
    efficiency_score: float        # 0.0-1.0
    completion_score: float        # 0.0-1.0
    loops_detected: List[str]      # node names that looped
    dead_end_detected: bool
    expected_end_node: Optional[str]
    actual_end_node: Optional[str]
    node_visits: List[NodeVisit]
    explanation: str


class TrajectoryScorer:
    """Scores a LangGraph trajectory based on efficiency, completion, loops, and dead-ends."""

    def __init__(self):
        """Initialize the TrajectoryScorer."""
        pass

    def score(self, node_sequence: List[str], expected_end_node: str = None, max_loops: int = 3) -> TrajectoryReport:
        """
        Score a trajectory based on node sequence.

        Args:
            node_sequence: List of node names in execution order
            expected_end_node: Expected final node name (optional)
            max_loops: Maximum times a node can appear before being considered a loop

        Returns:
            TrajectoryReport with scores and analysis
        """
        if not node_sequence:
            return self._empty_report(expected_end_node)

        # Count visits per node
        visit_counts: Dict[str, int] = {}
        for node_name in node_sequence:
            visit_counts[node_name] = visit_counts.get(node_name, 0) + 1

        # Create NodeVisit list with first occurrence order
        node_visits = []
        seen_nodes = set()
        for i, node_name in enumerate(node_sequence):
            if node_name not in seen_nodes:
                node_visits.append(NodeVisit(
                    node_name=node_name,
                    visit_count=visit_counts[node_name],
                    order=i
                ))
                seen_nodes.add(node_name)

        # Sort by first occurrence order
        node_visits.sort(key=lambda x: x.order)

        # Calculate efficiency score: 1.0 minus penalty for repeated nodes
        total_nodes = len(node_sequence)
        unique_nodes = len(set(node_sequence))
        if total_nodes > 0:
            # Penalty based on ratio of repeated nodes
            repetition_ratio = (total_nodes - unique_nodes) / total_nodes
            efficiency_score = max(0.0, 1.0 - repetition_ratio)
        else:
            efficiency_score = 0.0

        # Calculate completion score
        actual_end_node = node_sequence[-1] if node_sequence else None
        if expected_end_node is None:
            completion_score = 1.0  # No expectation means success
        else:
            completion_score = 1.0 if actual_end_node == expected_end_node else 0.0

        # Detect loops: nodes appearing more than max_loops times
        loops_detected = [
            node_name for node_name, count in visit_counts.items()
            if count > max_loops
        ]

        # Detect dead-end: ended on unexpected node (when expectation is set)
        dead_end_detected = False
        if expected_end_node is not None and actual_end_node != expected_end_node:
            dead_end_detected = True

        # Generate explanation
        explanation_parts = []
        explanation_parts.append(f"Trajectory length: {total_nodes} steps")
        explanation_parts.append(f"Unique nodes visited: {unique_nodes}")

        if loops_detected:
            explanation_parts.append(f"Loops detected in: {', '.join(loops_detected)}")
        else:
            explanation_parts.append("No loops detected")

        if expected_end_node:
            explanation_parts.append(f"Expected end: {expected_end_node}, Actual end: {actual_end_node}")
            if actual_end_node == expected_end_node:
                explanation_parts.append("Successfully reached expected end node")
            else:
                explanation_parts.append("Did not reach expected end node")
        else:
            explanation_parts.append(f"Ended at: {actual_end_node}")

        explanation = ". ".join(explanation_parts) + "."

        return TrajectoryReport(
            efficiency_score=efficiency_score,
            completion_score=completion_score,
            loops_detected=loops_detected,
            dead_end_detected=dead_end_detected,
            expected_end_node=expected_end_node,
            actual_end_node=actual_end_node,
            node_visits=node_visits,
            explanation=explanation
        )

    def _empty_report(self, expected_end_node: Optional[str]) -> TrajectoryReport:
        """Return an empty report for when no nodes are found."""
        return TrajectoryReport(
            efficiency_score=0.0,
            completion_score=0.0 if expected_end_node else 1.0,
            loops_detected=[],
            dead_end_detected=bool(expected_end_node),
            expected_end_node=expected_end_node,
            actual_end_node=None,
            node_visits=[],
            explanation="No nodes found in trajectory."
        )
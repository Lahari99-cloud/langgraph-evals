"""
CLI entry point for the Trajectory Tracer TUI demo.
"""
import sys
from rich.console import Console
from .tracer import TrajectoryTracer
from ..core.failure_classifier import FailureClassifier, FailureResult


def main():
    """Run the TUI demo."""
    tracer = TrajectoryTracer()
    classifier = FailureClassifier()
    console = Console()

    console.print("[bold]langgraph-evals Trajectory Tracer Demo[/bold]\n")

    # Demo 1: Perfect run
    console.print("[bold blue]Demo 1: Perfect trajectory[/bold blue]")
    tracer.display(
        node_sequence=["start", "process", "validate", "end"],
        scores={"efficiency": 1.0, "completion": 1.0}
    )

    # Demo 2: Loop overflow
    console.print("[bold blue]Demo 2: Loop overflow detected[/bold blue]")
    loop_result = FailureResult(
        name="LOOP_OVERFLOW",
        description="Node executed too many times in a loop",
        evidence={"node": "process", "count": 5, "max_allowed": 3},
        remediation="Check loop conditions or add circuit breaker",
    )
    tracer.display(
        node_sequence=["start", "process", "process", "process", "process", "process", "end"],
        failure_result=loop_result,
        scores={"efficiency": 0.4, "completion": 1.0}
    )

    # Demo 3: Premature termination
    console.print("[bold blue]Demo 3: Premature termination[/bold blue]")
    premature_result = FailureResult(
        name="PREMATURE_TERMINATION",
        description="Agent terminated before reaching END node",
        evidence={"last_node": "error_handler", "expected": "end"},
        remediation="Ensure all execution paths lead to END state",
    )
    tracer.display(
        node_sequence=["start", "process", "error_handler"],
        failure_result=premature_result,
        scores={"efficiency": 0.6, "completion": 0.0}
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
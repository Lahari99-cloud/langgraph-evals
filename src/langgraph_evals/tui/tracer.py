"""
Trajectory Tracer TUI for langgraph-evals
"""
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text
from typing import List, Optional, Dict, Any
from ..core.failure_classifier import FailureResult


class TrajectoryTracer:
    """Rich-based terminal UI for visualizing LangGraph trajectories."""

    def __init__(self):
        self.console = Console()

    def display(
        self,
        node_sequence: List[str],
        failure_result: Optional[FailureResult] = None,
        scores: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Display a trajectory trace with Rich formatting.

        Args:
            node_sequence: List of node names in order of execution.
            failure_result: Optional FailureResult from FailureClassifier.
            scores: Optional dict with keys 'efficiency' and 'completion'.
        """
        if scores is None:
            scores = {}

        # Build the visual tree
        tree = Tree("START")
        current = tree

        # Count consecutive repeats
        if not node_sequence:
            # Empty sequence
            current.add("[dim]No nodes[/dim]")
        else:
            prev_node = None
            count = 1
            for i, node in enumerate(node_sequence):
                if i == 0:
                    prev_node = node
                    continue
                if node == prev_node:
                    count += 1
                else:
                    # Add the previous node with count if >1
                    if count > 1:
                        label = f"{prev_node} [red][x{count}]❌[/red]"
                    else:
                        label = f"{prev_node}"
                    current.add(label)
                    # Start a new branch
                    current = tree
                    # We need to add nodes sequentially; simpler: just add each node
                    # Let's reset approach: we'll build a flat list and then convert to tree with repeats
                    break
            else:
                # Handle the last node
                if count > 1:
                    label = f"{prev_node} [red][x{count}]❌[/red]"
                else:
                    label = f"{prev_node}"
                current.add(label)

        # Actually, let's do a simpler approach: just show the sequence with arrows
        # and mark repeats
        self.console.print()
        if not node_sequence:
            self.console.print("[dim]START -> END (no nodes)[/dim]")
        else:
            # Build the path string
            path_parts = []
            i = 0
            while i < len(node_sequence):
                node = node_sequence[i]
                count = 1
                j = i + 1
                while j < len(node_sequence) and node_sequence[j] == node:
                    count += 1
                    j += 1
                if count > 1:
                    path_parts.append(f"{node} [red][x{count}][LOOP][/red]")
                else:
                    path_parts.append(node)
                i = j
            path_str = " START -> " + " -> ".join(path_parts) + " -> END"
            self.console.print(path_str)

        # Scores panel
        efficiency = scores.get("efficiency", 0.0)
        completion = scores.get("completion", 0.0)

        # Determine colors
        def score_color(score):
            if score > 0.8:
                return "green"
            elif score > 0.5:
                return "yellow"
            else:
                return "red"

        efficiency_color = score_color(efficiency)
        completion_color = "green" if completion >= 1.0 else "red"

        panel_content = []
        panel_content.append(
            f"Efficiency: [{efficiency_color}]{efficiency:.2f}[/{efficiency_color}]"
        )
        panel_content.append(
            f"Completion: [{completion_color}]{completion:.2f}[/{completion_color}]"
        )
        if failure_result:
            panel_content.append(
                f"[bold red]Failure:[/bold red] {failure_result.name}"
            )
            panel_content.append(
                f"[yellow]Remediation:[/yellow] {failure_result.remediation}"
            )

        self.console.print(
            Panel(
                "\n".join(panel_content),
                title="Trace Analysis",
                border_style="blue",
            )
        )

        # Summary line
        if failure_result:
            self.console.print(f"[red]FAILURE: {failure_result.name} detected[/red]")
        else:
            self.console.print("[green]SUCCESS: Agent completed successfully[/green]")
        self.console.print()
"""Console reporter for LangGraph evaluations."""
import json
from datetime import datetime
from typing import Dict, Any

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ConsoleReporter:
    """Console reporter for LangGraph evaluation results."""

    def __init__(self):
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def report(self, results: Dict[str, Any]) -> None:
        """
        Report evaluation results to console.

        Args:
            results: Dictionary containing evaluation results
        """
        if not RICH_AVAILABLE:
            # Fallback to basic print if Rich is not available
            self._basic_report(results)
            return

        # Clear screen and create header
        self.console.print()
        self.console.rule("[bold blue]LangGraph Evaluation Report[/bold blue]")

        # Print timestamp
        timestamp = results.get('timestamp', datetime.now().isoformat())
        self.console.print(f"[dim]Timestamp: {timestamp}[/dim]")
        self.console.print()

        # Print graph info if available
        if 'graph' in results:
            self.console.print(f"[bold]Graph:[/bold] {results['graph']}")
            self.console.print()

        # Print assertions results
        if 'assertions' in results and results['assertions']:
            self._print_assertions_table(results['assertions'])
            self.console.print()

        # Print trajectory score if available
        if 'trajectory' in results and results['trajectory']:
            self._print_trajectory_panel(results['trajectory'])
            self.console.print()

        # Print failures if available
        if 'failures' in results and results['failures']:
            self._print_failures_panel(results['failures'])
            self.console.print()

        # Print summary
        if 'summary' in results and results['summary'] is not None:
            self._print_summary_panel(results['summary'])
        else:
            # Calculate summary from results if not provided
            assertions = results.get('assertions', {}) or {}
            passed = sum(1 for v in assertions.values() if v is True)
            failed = sum(1 for v in assertions.values() if v is False)
            total = passed + failed
            self._print_summary_panel({
                'total': total,
                'passed': passed,
                'failed': failed,
                'success_rate': passed / total if total > 0 else 0.0
            })

        self.console.print()
        self.console.rule("[bold blue]End Report[/bold blue]")
        self.console.print()

    def _print_assertions_table(self, assertions: Dict[str, Any]) -> None:
        """Print assertions results in a table."""
        if not assertions:
            return

        table = Table(title="Assertion Results", show_header=True, header_style="bold magenta")
        table.add_column("Assertion", style="cyan", no_wrap=True)
        table.add_column("Result", justify="center")
        table.add_column("Details", style="dim")

        for name, result in assertions.items():
            if result is True:
                result_text = "[green]PASS[/green]"
                details = ""
            elif result is False:
                result_text = "[red]FAIL[/red]"
                details = ""
            else:
                result_text = f"[yellow]{result}[/yellow]"
                details = str(result) if result not in [True, False] else ""

            table.add_row(name, result_text, details)

        self.console.print(table)

    def _print_trajectory_panel(self, trajectory: Dict[str, Any]) -> None:
        """Print trajectory score in a panel."""
        if not trajectory:
            return

        content = []
        if 'efficiency_score' in trajectory:
            content.append(f"Efficiency: {trajectory['efficiency_score']:.2f}")
        if 'completion_score' in trajectory:
            content.append(f"Completion: {trajectory['completion_score']:.2f}")
        if 'loops_detected' in trajectory:
            content.append(f"Loops: {trajectory['loops_detected']}")
        if 'dead_end_detected' in trajectory:
            content.append(f"Dead End: {'Yes' if trajectory['dead_end_detected'] else 'No'}")

        if content:
            panel = Panel(
                "\n".join(content),
                title="[bold]Trajectory Score[/bold]",
                border_style="blue"
            )
            self.console.print(panel)

    def _print_failures_panel(self, failures: Dict[str, Any]) -> None:
        """Print failures in a panel."""
        if not failures:
            return

        content = []
        for failure_type, failure_info in failures.items():
            if isinstance(failure_info, dict):
                name = failure_info.get('name', failure_type)
                desc = failure_info.get('description', '')
                evidence = failure_info.get('evidence', '')
                content.append(f"[red]{name}[/red]: {desc}")
                if evidence:
                    content.append(f"  Evidence: {evidence}")
            else:
                content.append(f"[red]{failure_type}[/red]: {failure_info}")

        if content:
            panel = Panel(
                "\n".join(content),
                title="[bold red]Failures Detected[/bold red]",
                border_style="red"
            )
            self.console.print(panel)

    def _print_summary_panel(self, summary: Dict[str, Any]) -> None:
        """Print summary in a panel."""
        # Handle None or invalid summary
        if not summary:
            summary = {}

        content = []
        content.append(f"Total Tests: {summary.get('total', 0)}")
        content.append(f"Passed: [green]{summary.get('passed', 0)}[/green]")
        content.append(f"Failed: [red]{summary.get('failed', 0)}[/red]")

        if 'success_rate' in summary:
            rate = summary['success_rate']
            color = "green" if rate >= 0.8 else "yellow" if rate >= 0.6 else "red"
            content.append(f"Success Rate: [{color}]{rate:.1%}[/{color}]")

        panel = Panel(
            "\n".join(content),
            title="[bold]Summary[/bold]",
            border_style="green" if summary.get('failed', 0) == 0 else "red"
        )
        self.console.print(panel)

    def _basic_report(self, results: Dict[str, Any]) -> None:
        """Fallback basic report when Rich is not available."""
        print("=" * 50)
        print("LangGraph Evaluation Report")
        print("=" * 50)
        print(f"Timestamp: {results.get('timestamp', 'unknown')}")
        print()

        if 'graph' in results:
            print(f"Graph: {results['graph']}")
            print()

        assertions = results.get('assertions', {}) or {}
        if assertions:
            print("Assertions:")
            for name, result in assertions.items():
                status = "PASS" if result is True else "FAIL" if result is False else str(result)
                print(f"  {name}: {status}")
            print()

        trajectory = results.get('trajectory', {}) or {}
        if trajectory:
            print("Trajectory:")
            for key, value in trajectory.items():
                print(f"  {key}: {value}")
            print()

        failures = results.get('failures', {}) or {}
        if failures:
            print("Failures:")
            for failure_type, failure_info in failures.items():
                print(f"  {failure_type}: {failure_info}")
            print()

        summary = results.get('summary') or self._calculate_summary(results)
        print("Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

        print("=" * 50)

    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate summary statistics from results.

        Args:
            results: Dictionary containing evaluation results

        Returns:
            Summary dictionary
        """
        assertions = results.get('assertions', {}) or {}
        total = len(assertions)
        passed = sum(1 for v in assertions.values() if v is True)
        failed = sum(1 for v in assertions.values() if v is False)
        success_rate = passed / total if total > 0 else 0.0

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "success_rate": success_rate
        }
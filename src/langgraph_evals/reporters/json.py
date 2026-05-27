"""JSON reporter for LangGraph evaluations."""
import json
from datetime import datetime
from typing import Dict, Any, Optional


class JsonReporter:
    """JSON reporter for LangGraph evaluation results."""

    def report(self, results: Dict[str, Any], output_path: str) -> Dict[str, Any]:
        """
        Report evaluation results to JSON file.

        Args:
            results: Dictionary containing evaluation results
            output_path: Path to write the JSON report

        Returns:
            The report dictionary that was written to file
        """
        # Build the report structure
        report_data = {
            "graph": results.get("graph", "unknown"),
            "timestamp": results.get("timestamp", datetime.now().isoformat()),
            "assertions": results.get("assertions", {}),
            "trajectory": results.get("trajectory", {}),
            "failures": results.get("failures", {}),
            "summary": results.get("summary", self._calculate_summary(results))
        }

        # Write to file
        try:
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2, sort_keys=True)
        except Exception as e:
            # Re-raise with more context
            raise IOError(f"Failed to write JSON report to {output_path}: {str(e)}")

        return report_data

    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate summary statistics from results.

        Args:
            results: Dictionary containing evaluation results

        Returns:
            Summary dictionary
        """
        assertions = results.get('assertions', {})
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
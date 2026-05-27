from dataclasses import dataclass
from collections import Counter
from typing import Any, Dict, List, Optional


@dataclass
class FailureResult:
    name: str
    description: str
    evidence: str
    remediation: str


class FailureClassifier:

    def classify(self, trace: List[Dict[str, Any]],
                 expected_end_node: str = "END",
                 max_loops: int = 3,
                 model_token_limit: int = 8192):

        if not trace:
            return FailureResult(
                name="PREMATURE_TERMINATION",
                description="END node never reached",
                evidence="No trace entries found",
                remediation="Ensure graph is invoked with valid input"
            )

        last_node = trace[-1].get("node_name")

        counts = Counter(t.get("node_name") for t in trace)
        for node, count in counts.items():
            if count > max_loops:
                return FailureResult(
                    name="LOOP_OVERFLOW",
                    description="any node appears more than max_loops times",
                    evidence=f"Node execution counts: {dict(counts)}",
                    remediation="Add loop detection and termination conditions"
                )

        for i, t in enumerate(trace):
            state = t.get("state", "")
            output = t.get("output", "")
            if state and output and str(state) not in str(output):
                return FailureResult(
                    name="LOST_IN_MIDDLE",
                    description="context in state but not referenced in output",
                    evidence=f"State length: {len(str(state))}, output does not reference state content",
                    remediation="Improve output generation to include retrieved context"
                )

        for t in trace:
            tool_calls = t.get("tool_calls", [])
            input_text = str(t.get("input", ""))
            for call in tool_calls:
                params = call.get("parameters", {})
                if isinstance(params, dict):
                    for val in params.values():
                        if str(val) not in input_text:
                            return FailureResult(
                                name="TOOL_HALLUCINATION",
                                description="tool calls contain parameters not in input",
                                evidence=f"Tool call parameters: {params} not found in input",
                                remediation="Validate tool parameters against input before execution"
                            )

        for t in trace:
            input_text = str(t.get("input", ""))
            estimated_tokens = len(input_text) // 4
            if estimated_tokens > model_token_limit * 0.8:
                return FailureResult(
                    name="CONTEXT_OVERFLOW",
                    description="input token count exceeds 80% of model limit",
                    evidence=f"Input length: {len(input_text)} chars (~{estimated_tokens} tokens), limit: {model_token_limit}",
                    remediation="Truncate or summarize input before passing to model"
                )

        thread_ids = [t.get("thread_id") for t in trace if t.get("thread_id")]
        if len(set(thread_ids)) > 1:
            return FailureResult(
                name="MEMORY_BLEED",
                description="state contains keys from a different thread_id",
                evidence=f"Thread IDs found: {set(thread_ids)}",
                remediation="Ensure proper thread isolation in checkpointer configuration"
            )

        if expected_end_node and last_node and last_node != expected_end_node and expected_end_node != "END":
            return FailureResult(
                name="WRONG_BRANCH",
                description="actual end node differs from expected end node",
                evidence=f"Actual end node: {last_node}, expected: {expected_end_node}",
                remediation="Review graph routing logic and conditional edges"
            )

        if last_node and last_node.upper() != "END":
            return FailureResult(
                name="PREMATURE_TERMINATION",
                description="END node never reached",
                evidence=f"Last node executed: {last_node}",
                remediation="Ensure graph has proper termination conditions"
            )

        return None

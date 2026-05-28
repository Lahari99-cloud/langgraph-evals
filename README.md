# langgraph-evals
Local-first evaluation harness for LangGraph agents.
No LangSmith. No cloud. No cost.

![Tests](https://img.shields.io/badge/tests-42%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Zero Egress](https://img.shields.io/badge/network-zero%20egress-important)
![Demo](docs/demo.gif)

## Why not LangSmith?
| Feature | LangSmith | langgraph-evals |
|---|---|---|
| Vendor-agnostic | ❌ | ✅ |
| Runs fully offline | ❌ | ✅ |
| Free forever | ❌ | ✅ |
| Works in air-gapped CI | ❌ | ✅ |
| Built-in failure taxonomy | ❌ | ✅ |
| Memory persistence testing | ❌ | ✅ |

## Install
pip install langgraph-evals

## Quickstart
```python
from langgraph_evals.core.assertions import assert_node_called, assert_node_order
from langgraph_evals.core.trajectory import TrajectoryScorer
from langgraph_evals.core.failure_classifier import FailureClassifier

graph_run = {
    "nodes_visited": ["start", "process", "end"],
    "tool_calls": [],
    "outputs": {"result": "done"}
}

assert_node_called(graph_run, "process")
assert_node_order(graph_run, ["start", "process", "end"])

scorer = TrajectoryScorer()
report = scorer.score(["start", "process", "end"], expected_end_node="end")
print(f"Efficiency: {report.efficiency_score}")
print(f"Completion: {report.completion_score}")

classifier = FailureClassifier()
result = classifier.classify([{"node_name": "start"}, {"node_name": "process"}])
if result:
    print(f"Failure: {result.name} — {result.remediation}")
```

## Core Features
- Node Assertions (6 functions)
- Trajectory Scoring
- Memory Persistence Testing
- Failure Taxonomy: LOST_IN_MIDDLE, TOOL_HALLUCINATION,
  CONTEXT_OVERFLOW, WRONG_BRANCH, MEMORY_BLEED,
  LOOP_OVERFLOW, PREMATURE_TERMINATION

## Regulated Environments
Built by engineers who've worked in regulated financial and telecom
environments where sending traces to external SaaS is not an option.
"Works where LangSmith is blocked by security policy.
JPMorgan, Amex, insurance, government contractors."
```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - run: pip install langgraph-evals
      - run: pytest --lge-report
```

## Contributing
PRs welcome. Open an issue first for major changes.
Contributions especially welcome for new failure taxonomy types
and domain-specific eval benchmarks (fintech, telecom, healthcare).

## License
MIT
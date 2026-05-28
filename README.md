# langgraph-evals
Local-first evaluation harness for LangGraph agents.
No LangSmith. No cloud. No cost.

![Tests](https://img.shields.io/badge/tests-45%20passed-brightgreen)
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

## Why does this exist?

LangSmith is LangChain's commercial monetization engine.
Building a robust free offline eval harness into the open-source
library would undercut enterprise SaaS subscriptions — so they didn't.

Meanwhile three things happened simultaneously:

1. **Enterprises adopted LangGraph** — JPMorgan, Amex, insurance,
   defense contractors. Their security policies block cloud telemetry
   completely. They had no way to eval their agents in CI.

2. **The industry realized agents fail structurally, not just semantically**
   — infinite loops, wrong conditional branches, tool hallucinations,
   memory bleed. These are code bugs, not text quality issues.
   pytest-style assertions catch them. LLM-as-a-judge doesn't.

3. **LangGraph's graph architecture made local tracing hard** —
   cyclical states, conditional edges, long-term memory. Nobody had
   reverse-engineered a clean interception layer until now.

`langgraph-evals` fills the gap: deterministic, structural,
fully offline evaluation for LangGraph agents.

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
# PR Security Agent — Finance & Banking Use Case

Built for regulated environments where code review agents must be evaluated locally without cloud telemetry.

This example demonstrates a real LangGraph StateGraph agent that performs security scanning on pull requests, integrating with langgraph-evals for trajectory tracing and failure classification.

## How It Works

The agent consists of four nodes:
1. **supervisor** — Routes incoming PR to correct scanner
2. **security_scan** — Checks for hardcoded secrets, SQL injection, exposed API keys in code diff
3. **quality_check** — Checks for missing tests, TODO comments
4. **analytics_eval** — Uses langgraph-evals TrajectoryTracer to visualize the run and FailureClassifier to detect issues

The agent implements loop prevention with MAX_LOOP_LIMIT = 3 to prevent infinite loops when security issues are found.

## langgraph-evals Integration

This example showcases two critical integrations with langgraph-evals:

### 1. Trajectory Visualization
The `analytics_eval` node prepares data for the TrajectoryTracer, which creates rich terminal visualizations of agent execution paths.

### 2. Failure Detection
The FailureClassifier analyzes the execution trace to detect issues like:
- **LOOP_OVERFLOW**: When nodes are executed too many times (indicating ineffective remediation loops)
- Other failure types: LOST_IN_MIDDLE, TOOL_HALLUCINATION, CONTEXT_OVERFLOW, WRONG_BRANCH, MEMORY_BLEED, PREMATURE_TERMINATION

In regulated environments (finance, banking, healthcare, government), this local evaluation capability is essential because:
- No cloud telemetry can be sent due to security policies
- Agents must be fully auditable and explainable
- Failure detection must happen in air-gapped CI systems

## Key Features

✅ **Real LangGraph StateGraph** - Uses actual StateGraph execution, not mocks
✅ **langgraph-evals Integration** - Uses GraphRunCapture, TrajectoryScorer, and FailureClassifier
✅ **Loop Prevention** - Configurable MAX_LOOP_LIMIT prevents infinite loops
✅ **Regulated Environment Ready** - Zero external dependencies, fully offline
✅ **Rich Terminal Output** - Visual trajectory tracing with failure detection

## Running the Example

```bash
python examples/05_pr_security_agent/test_pr_agent.py
```

Or with pytest:
```bash
pytest examples/05_pr_security_agent/ -v
```

## Sample Output

When running tests, you'll see output like:
```
PR Security Agent — Finance & Banking Use Case
Testing clean PR...
[green]SUCCESS: Agent completed successfully[/green]
Testing PR with hardcoded secret...
[red]FAILURE: LOOP_OVERFLOW detected[/red]
Testing PR with SQL injection...
[green]SUCCESS: Agent completed successfully[/green]
```

This demonstrates how langgraph-evals catches LOOP_OVERFLOW in real agents that get stuck in remediation loops, a common issue in automated security agents that keep finding the same issues without effective fixes.
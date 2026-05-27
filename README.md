# langgraph-evals

Evaluation framework for LangGraph applications.

## Features

- **Assertion Utilities**: Validate node calls, outputs, order, and tool usage
- **Trajectory Scoring**: Score graph runs on efficiency, completion, loops, and dead-ends
- **Pytest Plugin**: Automatic registration for easy testing
- **Flexible Design**: Works with various LangGraph run formats

## Installation

```bash
pip install langgraph-evals
```

## Development

```bash
pip install -e .[dev]
```

## Usage

### Assertions

```python
from langgraph_evals.core.runner import (
    assert_node_called,
    assert_node_output,
    assert_node_order,
    assert_no_node_called,
    assert_tool_called,
    assert_tool_not_called
)

# Assuming `trajectory` is your LangGraph run data
assert_node_called(trajectory, "my_node")
assert_node_output(trajectory, "my_node", "result", "success")
assert_node_order(trajectory, ["start", "process", "end"])
assert_no_node_called(trajectory, "error_handler")
assert_tool_called(trajectory, "search_tool")
assert_tool_not_called(trajectory, "delete_tool")
```

### Trajectory Scoring

```python
from langgraph_evals.core.trajectory import TrajectoryScorer

scorer = TrajectoryScorer()
# For a simple list of node names in order
node_sequence = ['start', 'process', 'end']

report = scorer.score(node_sequence, expected_end_node='end')
print(f"Efficiency: {report.efficiency_score}")
print(f"Completion: {report.completion_score}")
print(f"Loops: {report.loops_detected}")
print(f"Dead end: {report.dead_end_detected}")

# Custom loop threshold (default is 3)
report = scorer.score(node_sequence, expected_end_node='end', max_loops=1)
```

## Running Tests

```bash
pytest
```

## License

MIT
# Real LangGraph Integration Example

This example demonstrates how to use langgraph-evals with actual LangGraph StateGraph executions, closing the gap where assertions only worked on mock data.

## Files

- `agent.py`: A simple LangGraph agent (similar to the first example)
- `test_real_agent.py`: Test showing how to use `GraphRunCapture` to capture real graph executions and apply langgraph-evals assertions

## How it Works

The `GraphRunCapture` context manager wraps a LangGraph StateGraph's `invoke` method to capture:

- Node visits (as `nodes_visited` list)
- Tool calls (as `tool_calls` list)
- Node outputs (as `outputs` dict)
- Final state

This captured data is in the exact format expected by langgraph-evals assertion functions like `assert_node_called`, `assert_node_order`, etc.

## Running the Example

```bash
python examples/04_langgraph_integration/test_real_agent.py
```

Or with pytest:
```bash
pytest examples/04_langgraph_integration/ -v
```
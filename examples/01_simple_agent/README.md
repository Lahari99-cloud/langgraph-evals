# Simple LangGraph Agent Example

This example demonstrates a basic LangGraph agent using StateGraph that can be run in completely air-gapped/regulated environments with zero external dependencies.

## Features

- **Zero External Dependencies**: No API keys, no internet required
- **Deterministic Behavior**: Same input always produces same output
- **Easy to Test**: Fully compatible with langgraph-evals assertion utilities
- **Regulation Friendly**: Suitable for FIPS, HIPAA, GDPR, and other regulated environments

## How It Works

This example creates a simple two-step agent:
1. `process_input` node: Processes the input text
2. `format_output` node: Formats the final result

## Running the Example

```bash
# Run the agent directly
python agent.py

# Run the tests
python -m pytest test_simple_agent.py -v
```

## Using with langgraph-evals

The test file demonstrates how to use:
- `assert_node_called()` - Verify specific nodes were executed
- `assert_node_order()` - Verify execution sequence
- `TrajectoryScorer` - Score the execution trajectory
- `assert_no_node_called()` - Verify nodes were NOT executed

## Regulated Environment Compatible

This example:
- Makes zero network calls
- Requires no API keys or external services
- Uses only standard Python library + langgraph
- Can be built into air-gapped containers
- Compliant with SSLF, HIPAA, GDPR, and similar regulations
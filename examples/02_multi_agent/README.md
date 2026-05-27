# Multi-Agent LangGraph Example with Memory Isolation

This example demonstrates a supervisor-worker multi-agent LangGraph pattern designed for air-gapped/regulated environments with **zero external dependencies**.

## Features

- **Supervisor-Worker Pattern**: Clear separation of concerns
- **Memory Isolation Testing**: Demonstrates how to test thread isolation with langgraph-evals
- **Zero External Dependencies**: No API keys, no internet required
- **Deterministic Behavior**: Same input always produces same output
- **Regulation Friendly**: Suitable for secure/compliant environments

## How It Works

This example creates a three-node agent system:
1. `supervisor` node: Receives input and delegates to worker
2. `worker` node: Processes the input and returns results
3. `output` node: Formats and returns the final result

The example includes both:
- Basic usage (without memory checkpointing)
- Memory-enabled version (for isolation testing)

## Running the Examples

```bash
# Run the agent directly to see the supervisor-worker pattern
python agents.py

# Run the tests
python -m pytest test_multi_agent.py -v
```

## Using with langgraph-evals for Memory Isolation Testing

The test file demonstrates how to use:
- `assert_memory_isolated()` - Verify that memory is properly isolated between threads
- Checkpointer pattern with `MemorySaver` for thread-specific state
- Thread ID configuration to separate conversation states

## Regulated Environment Compatible

This example:
- Makes zero network calls
- Requires no API keys or external services
- Uses only standard Python library + langgraph
- Can be built into air-gapped containers
- Compliant with SSLF, HIPAA, GDPR, and similar regulations
- Demonstrates proper memory isolation for regulated workloads
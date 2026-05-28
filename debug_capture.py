"""Debug script to see what's actually captured."""
import importlib.util
import sys

# Load the agent module from the examples directory
spec = importlib.util.spec_from_file_location(
    "simple_agent",
    "examples/01_simple_agent/agent.py"
)
simple_agent_module = importlib.util.module_from_spec(spec)
sys.modules["simple_agent"] = simple_agent_module
spec.loader.exec_module(simple_agent_module)

from langgraph_evals.langgraph.runner import GraphRunCapture

# Create the agent
agent = simple_agent_module.create_simple_agent()

print("Testing GraphRunCapture...")
with GraphRunCapture(agent, {"input": "test", "steps": [], "result": None}) as captured_run:
    print("Inside context manager:")
    print("  captured_run type:", type(captured_run))
    print("  captured_run keys:", list(captured_run.keys()) if isinstance(captured_run, dict) else "Not a dict")
    for key, value in captured_run.items():
        print(f"  {key}: {value}")

    # Invoke the agent
    result = agent.invoke({"input": "hello world", "steps": [], "result": None})
    print("\nAfter invoke:")
    print("  result:", result)
    print("  captured_run after invoke:", captured_run)

print("\nOutside context manager:")
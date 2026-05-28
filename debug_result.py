"""Debug script to see what the simple agent actually returns."""
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

# Create the agent
agent = simple_agent_module.create_simple_agent()

# Invoke the agent
result = agent.invoke({"input": "hello world", "steps": [], "result": None})

print("Result type:", type(result))
print("Result:", result)
print("Result keys:", list(result.keys()) if isinstance(result, dict) else "Not a dict")

if isinstance(result, dict):
    for key, value in result.items():
        print(f"  {key}: {value} (type: {type(value)})")
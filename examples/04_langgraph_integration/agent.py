"""
Simple LangGraph agent for demonstrating real LangGraph integration.
This is similar to the agent in examples/01_simple_agent but standalone.
"""
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """State for our simple agent."""
    input: str
    steps: List[str]
    result: Optional[str]


def process_input(state: AgentState) -> AgentState:
    """Process the input and add a step."""
    steps = state["steps"] + ["process_input"]
    return {
        **state,
        "steps": steps,
        "result": f"Processed: {state['input']}"
    }


def format_output(state: AgentState) -> AgentState:
    """Format the final output."""
    steps = state["steps"] + ["format_output"]
    return {
        **state,
        "steps": steps,
        "result": f"RESULT: {state['result']}"
    }


def create_agent() -> StateGraph:
    """Create and return a simple LangGraph agent."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("process_input", process_input)
    workflow.add_node("format_output", format_output)

    # Set entry point
    workflow.set_entry_point("process_input")

    # Add edges
    workflow.add_edge("process_input", "format_output")
    workflow.add_edge("format_output", END)

    # Compile the graph
    return workflow.compile()


# Example usage
if __name__ == "__main__":
    # Create the agent
    agent = create_agent()

    # Invoke the agent
    initial_state = {
        "input": "Hello, World!",
        "steps": [],
        "result": None
    }

    result = agent.invoke(initial_state)
    print(f"Final result: {result['result']}")
    print(f"Execution steps: {result['steps']}")
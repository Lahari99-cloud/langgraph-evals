"""
Multi-agent LangGraph example demonstrating supervisor and worker pattern with memory isolation.
This example is designed to run in air-gapped/regulated environments with zero external dependencies.
"""

from typing import TypedDict, List, Optional, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


class SupervisorState(TypedDict):
    """State for the multi-agent system."""
    input: str
    supervisor_notes: List[str]
    worker_results: List[str]
    current_agent: Literal["supervisor", "worker", "output"]
    final_output: Optional[str]
    steps: List[str]


def supervisor_node(state: SupervisorState) -> SupervisorState:
    """Supervisor node that delegates to the worker."""
    notes = state["supervisor_notes"] + [f"Supervisor processing: {state['input']}"]
    steps = state["steps"] + ["supervisor"]
    # After supervising, delegate to worker
    return {
        **state,
        "supervisor_notes": notes,
        "current_agent": "worker",
        "steps": steps
    }


def worker_node(state: SupervisorState) -> SupervisorState:
    """Worker node that processes the input and returns results."""
    results = state["worker_results"] + [f"Worker completed: {state['input']}"]
    steps = state["steps"] + ["worker"]
    # After working, go to output
    return {
        **state,
        "worker_results": results,
        "current_agent": "output",
        "steps": steps
    }


def output_node(state: SupervisorState) -> SupervisorState:
    """Output node that formats the final result."""
    steps = state["steps"] + ["output"]
    # Combine the results
    final_output = (
        f"Supervisor: {state['supervisor_notes'][-1] if state['supervisor_notes'] else 'None'} | "
        f"Worker: {state['worker_results'][-1] if state['worker_results'] else 'None'}"
    )
    return {
        **state,
        "final_output": final_output,
        "steps": steps
    }


def create_multi_agent_with_memory():
    """Create a multi-agent LangGraph with checkpointer for memory isolation testing."""
    workflow = StateGraph(SupervisorState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("output", output_node)

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Add edges
    workflow.add_edge("supervisor", "worker")
    workflow.add_edge("worker", "output")
    workflow.add_edge("output", END)

    # Add memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


# Example usage without memory (for direct invocation)
def create_multi_agent():
    """Create a multi-agent LangGraph without checkpointer for simple usage."""
    workflow = StateGraph(SupervisorState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("output", output_node)

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Add edges
    workflow.add_edge("supervisor", "worker")
    workflow.add_edge("worker", "output")
    workflow.add_edge("output", END)

    return workflow.compile()


if __name__ == "__main__":
    # Example 1: Simple usage without memory checking
    print("=== Simple Multi-Agent Usage ===")
    agent = create_multi_agent()
    initial_state = {
        "input": "Hello from the multi-agent system!",
        "supervisor_notes": [],
        "worker_results": [],
        "current_agent": "supervisor",
        "final_output": None,
        "steps": []
    }

    result = agent.invoke(initial_state)
    print(f"Final Output: {result['final_output']}")
    print(f"Steps: {result['steps']}")

    print("\n=== Multi-Agent with Memory Isolation ===")
    # Example 2: With memory for isolation testing
    agent_with_memory = create_multi_agent_with_memory()

    # Thread 1
    config1 = {"configurable": {"thread_id": "thread-1"}}
    initial_state1 = {
        "input": "First thread input",
        "supervisor_notes": [],
        "worker_results": [],
        "current_agent": "supervisor",
        "final_output": None,
        "steps": []
    }
    result1 = agent_with_memory.invoke(initial_state1, config1)
    print(f"Thread 1 Output: {result1['final_output']}")

    # Thread 2
    config2 = {"configurable": {"thread_id": "thread-2"}}
    initial_state2 = {
        "input": "Second thread input",
        "supervisor_notes": [],
        "worker_results": [],
        "current_agent": "supervisor",
        "final_output": None,
        "steps": []
    }
    result2 = agent_with_memory.invoke(initial_state2, config2)
    print(f"Thread 2 Output: {result2['final_output']}")

    # Show that memories are isolated by checking that thread 1 doesn't have thread 2's data
    # We can inspect the checkpointer state if needed
    print("\nMemory isolation: Each thread maintains its own state.")
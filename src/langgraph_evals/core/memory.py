"""Memory persistence testing for LangGraph agents."""

def assert_remembers(agent, turn1_input: str, turn2_query: str, expected_memory_key: str):
    """
    Assert that an agent remembers information from a previous turn.

    Args:
        agent: LangGraph agent with memory
        turn1_input: Input provided in first turn
        turn2_query: Query provided in second turn to test memory
        expected_memory_key: Expected key/value that should be remembered

    Raises:
        AssertionError: If the agent does not remember the expected information
    """
    # Execute first turn to store memory
    config_1 = {"configurable": {"thread_id": "turn1"}}
    result_1 = agent.invoke({"input": turn1_input}, config_1)

    # Execute second turn to test memory
    config_2 = {"configurable": {"thread_id": "turn2"}}
    result_2 = agent.invoke({"input": turn2_query}, config_2)

    # Extract output from results
    output_2 = str(result_2.get("output", "")) if isinstance(result_2, dict) else str(getattr(result_2, "output", ""))

    if expected_memory_key not in output_2:
        raise AssertionError(
            f"Expected agent to remember '{expected_memory_key}' from turn 1 input, "
            f"but it was not found in turn 2 output.\n"
            f"Turn 1 input: {turn1_input}\n"
            f"Turn 2 query: {turn2_query}\n"
            f"Turn 2 output: {output_2}"
        )


def assert_memory_isolated(agent, thread_id_1: str, thread_id_2: str,
                            input: str, memory_key: str):
    """
    Assert that memory is isolated between different threads/conversations.

    Args:
        agent: LangGraph agent with memory
        thread_id_1: First thread/conversation ID
        thread_id_2: Second thread/conversation ID (should be isolated)
        input: Input to provide in both threads
        memory_key: Key that should be remembered in thread_1 but not thread_2

    Raises:
        AssertionError: If memory is not properly isolated between threads
    """
    # Execute in first thread
    config_1 = {"configurable": {"thread_id": thread_id_1}}
    result_1 = agent.invoke({"input": input}, config_1)

    # Execute in second thread
    config_2 = {"configurable": {"thread_id": thread_id_2}}
    result_2 = agent.invoke({"input": input}, config_2)

    # Extract outputs
    output_1 = str(result_1.get("output", "")) if isinstance(result_1, dict) else str(getattr(result_1, "output", ""))
    output_2 = str(result_2.get("output", "")) if isinstance(result_2, dict) else str(getattr(result_2, "output", ""))

    if memory_key not in output_1:
        raise AssertionError(
            f"Expected memory_key '{memory_key}' to be present in thread {thread_id_1} output, "
            f"but it was not found.\n"
            f"Thread {thread_id_1} output: {output_1}"
        )

    if memory_key in output_2:
        raise AssertionError(
            f"Expected memory_key '{memory_key}' to be isolated in thread {thread_id_2}, "
            f"but it was found in the output.\n"
            f"Thread {thread_id_2} output: {output_2}"
        )


def assert_forgets(agent, input: str, after_n_turns: int, memory_key: str):
    """
    Assert that an agent forgets information after a specified number of turns.

    Args:
        agent: LangGraph agent with memory
        input: Input to provide initially
        after_n_turns: Number of turns after which memory should be forgotten
        memory_key: Key that should be forgotten after after_n_turns

    Raises:
        AssertionError: If the agent remembers when it should have forgotten
    """
    # Execute initial turn to store memory
    config_initial = {"configurable": {"thread_id": "initial"}}
    agent.invoke({"input": input}, config_initial)

    # Execute intermediate turns (if any)
    for i in range(after_n_turns):
        config_intermediate = {"configurable": {"thread_id": f"intermediate_{i}"}}
        agent.invoke({"input": f"intermediate_input_{i}"}, config_intermediate)

    # Execute final turn to test if memory is forgotten
    config_final = {"configurable": {"thread_id": "final"}}
    result_final = agent.invoke({"input": "test_forgetting"}, config_final)

    # Extract final output
    output_final = str(result_final.get("output", "")) if isinstance(result_final, dict) else str(getattr(result_final, "output", ""))

    if memory_key in output_final:
        raise AssertionError(
            f"Expected agent to forget '{memory_key}' after {after_n_turns} turns, "
            f"but it was still found in the output.\n"
            f"Final output: {output_final}"
        )
"""Tests for memory persistence functionality."""

import pytest
from unittest.mock import Mock

# Import the memory testing utilities
from langgraph_evals.core.memory import (
    assert_remembers,
    assert_memory_isolated,
    assert_forgets
)


def test_assert_remembers_basic():
    """Test that assert_remembers works when agent remembers correctly."""
    # Create a mock agent that simulates remembering
    mock_agent = Mock()

    # First call stores the information
    # Second call should return the remembered information
    mock_agent.invoke.side_effect = [
        {"output": "I learned that the user likes pizza"},  # First turn
        {"output": "Based on what you told me, you like pizza"}  # Second turn - remembers
    ]

    # This should pass - agent remembers "likes pizza"
    assert_remembers(
        mock_agent,
        turn1_input="I like pizza",
        turn2_query="What do I like?",
        expected_memory_key="pizza"
    )


def test_assert_remembers_fails_when_not_remembering():
    """Test that assert_remembers fails when agent doesn't remember."""
    # Create a mock agent that doesn't remember
    mock_agent = Mock()

    mock_agent.invoke.side_effect = [
        {"output": "I learned that the user likes pizza"},  # First turn
        {"output": "I don't recall what you like"}  # Second turn - doesn't remember
    ]

    # This should fail - agent doesn't remember "likes pizza"
    with pytest.raises(AssertionError, match="Expected agent to remember"):
        assert_remembers(
            mock_agent,
            turn1_input="I like pizza",
            turn2_query="What do I like?",
            expected_memory_key="pizza"
        )


def test_assert_memory_isolated_basic():
    """Test that assert_memory_isolated works when memory is properly isolated."""
    # Create a mock agent
    mock_agent = Mock()

    # Thread 1: stores memory
    # Thread 2: should not have access to thread 1's memory
    mock_agent.invoke.side_effect = [
        {"output": "I learned that the secret is blue"},  # Thread 1
        {"output": "I don't know any secrets"}  # Thread 2 - isolated
    ]

    # This should pass - memory is isolated
    assert_memory_isolated(
        mock_agent,
        thread_id_1="thread_1",
        thread_id_2="thread_2",
        input="The secret is blue",
        memory_key="blue"
    )


def test_assert_forgets_basic():
    """Test that assert_forgets works when agent forgets correctly."""
    # Create a mock agent
    mock_agent = Mock()

    # Initial turn: stores memory
    # Intermediate turns: agent processes other inputs
    # Final turn: agent should have forgotten
    mock_agent.invoke.side_effect = [
        {"output": "I learned that the password is swordfish"},  # Initial
        {"output": "Processing intermediate turn 1"},  # Intermediate 1
        {"output": "Processing intermediate turn 2"},  # Intermediate 2
        {"output": "I don't remember any passwords"}  # Final - forgot
    ]

    # This should pass - agent forgot after 2 turns
    assert_forgets(
        mock_agent,
        input="The password is swordfish",
        after_n_turns=2,
        memory_key="swordfish"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
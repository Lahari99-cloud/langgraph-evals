"""Assertion utilities for evaluating LangGraph trajectories."""

def assert_node_called(graph_run, node_name):
    """
    Assert that a specific node was called in the graph run.

    Args:
        graph_run: The graph run object/trajectory
        node_name: Name of the node to check

    Raises:
        AssertionError: If the node was not called
    """
    # Assuming graph_run has a 'nodes' attribute or similar
    nodes_called = getattr(graph_run, 'nodes', None)
    if nodes_called is None:
        # Try dictionary access
        nodes_called = graph_run.get('nodes', []) if isinstance(graph_run, dict) else []

    called_names = [node.get('name') if isinstance(node, dict) else getattr(node, 'name', None)
                   for node in nodes_called]

    if node_name not in called_names:
        raise AssertionError(
            f"Expected node '{node_name}' to be called, but it was not. "
            f"Called nodes: {called_names}"
        )


def assert_node_output(graph_run, node_name, key, expected_value):
    """
    Assert that a specific node produced an expected output value for a given key.

    Args:
        graph_run: The graph run object/trajectory
        node_name: Name of the node to check
        key: Key in the node's output to check
        expected_value: Expected value for the output key

    Raises:
        AssertionError: If the node was not called or output doesn't match
    """
    nodes_called = getattr(graph_run, 'nodes', None)
    if nodes_called is None:
        nodes_called = graph_run.get('nodes', []) if isinstance(graph_run, dict) else []

    # Find the node
    node_found = None
    for node in nodes_called:
        if isinstance(node, dict):
            if node.get('name') == node_name:
                node_found = node
                break
        else:
            if getattr(node, 'name', None) == node_name:
                node_found = node
                break

    if node_found is None:
        called_names = [n.get('name') if isinstance(n, dict) else getattr(n, 'name', None)
                       for n in nodes_called]
        raise AssertionError(
            f"Expected node '{node_name}' to be called, but it was not. "
            f"Called nodes: {called_names}"
        )

    # Get output
    output = node_found.get('output') if isinstance(node_found, dict) else getattr(node_found, 'output', None)
    if output is None:
        raise AssertionError(
            f"Node '{node_name}' has no output attribute."
        )

    actual_value = output.get(key) if isinstance(output, dict) else getattr(output, key, None)

    if actual_value != expected_value:
        raise AssertionError(
            f"Node '{node_name}' output mismatch for key '{key}'. "
            f"Expected: {expected_value!r}, Actual: {actual_value!r}"
        )


def assert_node_order(graph_run, expected_order):
    """
    Assert that nodes were called in a specific order.

    Args:
        graph_run: The graph run object/trajectory
        expected_order: List of node names in expected call order

    Raises:
        AssertionError: If nodes were not called in the expected order
    """
    nodes_called = getattr(graph_run, 'nodes', None)
    if nodes_called is None:
        nodes_called = graph_run.get('nodes', []) if isinstance(graph_run, dict) else []

    called_names = [node.get('name') if isinstance(node, dict) else getattr(node, 'name', None)
                   for node in nodes_called]

    # Filter to only nodes in expected_order to allow other nodes in between?
    # Based on typical assertion, we expect exact sequence match
    if called_names != expected_order:
        raise AssertionError(
            f"Node call order mismatch.\n"
            f"Expected: {expected_order}\n"
            f"Actual:   {called_names}"
        )


def assert_no_node_called(graph_run, node_name):
    """
    Assert that a specific node was NOT called in the graph run.

    Args:
        graph_run: The graph run object/trajectory
        node_name: Name of the node that should not have been called

    Raises:
        AssertionError: If the node was called when it shouldn't have been
    """
    nodes_called = getattr(graph_run, 'nodes', None)
    if nodes_called is None:
        nodes_called = graph_run.get('nodes', []) if isinstance(graph_run, dict) else []

    called_names = [node.get('name') if isinstance(node, dict) else getattr(node, 'name', None)
                   for node in nodes_called]

    if node_name in called_names:
        raise AssertionError(
            f"Expected node '{node_name}' to NOT be called, but it was called. "
            f"Called nodes: {called_names}"
        )


def assert_tool_called(graph_run, tool_name):
    """
    Assert that a specific tool was called during the graph run.

    Args:
        graph_run: The graph run object/trajectory
        tool_name: Name of the tool to check

    Raises:
        AssertionError: If the tool was not called
    """
    tool_calls = getattr(graph_run, 'tool_calls', None)
    if tool_calls is None:
        tool_calls = graph_run.get('tool_calls', []) if isinstance(graph_run, dict) else []

    called_tools = [call.get('name') if isinstance(call, dict) else getattr(call, 'name', None)
                   for call in tool_calls]

    if tool_name not in called_tools:
        raise AssertionError(
            f"Expected tool '{tool_name}' to be called, but it was not. "
            f"Called tools: {called_tools}"
        )


def assert_tool_not_called(graph_run, tool_name):
    """
    Assert that a specific tool was NOT called during the graph run.

    Args:
        graph_run: The graph run object/trajectory
        tool_name: Name of the tool that should not have been called

    Raises:
        AssertionError: If the tool was called when it shouldn't have been
    """
    tool_calls = getattr(graph_run, 'tool_calls', None)
    if tool_calls is None:
        tool_calls = graph_run.get('tool_calls', []) if isinstance(graph_run, dict) else []

    called_tools = [call.get('name') if isinstance(call, dict) else getattr(call, 'name', None)
                   for call in tool_calls]

    if tool_name in called_tools:
        raise AssertionError(
            f"Expected tool '{tool_name}' to NOT be called, but it was called. "
            f"Called tools: {called_tools}"
        )
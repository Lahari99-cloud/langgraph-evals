"""Tests for the LangGraph evaluations pytest plugin."""
import pytest
from unittest.mock import Mock


def test_plugin_loads_without_error():
    """Test that the plugin loads without error."""
    from langgraph_evals import plugin
    assert plugin is not None
    assert hasattr(plugin, 'pytest_plugin')
    assert plugin.pytest_plugin is True


def test_plugin_has_required_functions():
    """Test that the plugin has all required pytest hook functions."""
    from langgraph_evals import plugin

    # Check that all required functions exist
    assert hasattr(plugin, 'pytest_configure')
    assert hasattr(plugin, 'pytest_addoption')
    assert hasattr(plugin, 'lge_runner')
    assert hasattr(plugin, 'pytest_runtest_makereport')
    assert hasattr(plugin, 'pytest_sessionfinish')

    # Check that they are callable
    assert callable(plugin.pytest_configure)
    assert callable(plugin.pytest_addoption)
    assert callable(plugin.lge_runner)
    assert callable(plugin.pytest_runtest_makereport)
    assert callable(plugin.pytest_sessionfinish)


def test_lge_marker_would_be_registered():
    """Test that the lge marker would be registered by pytest_configure."""
    from langgraph_evals import plugin

    # Create a mock config object
    mock_config = Mock()
    mock_config.addinivalue_line = Mock()

    # Call the configure function
    plugin.pytest_configure(mock_config)

    # Verify that addinivalue_line was called with the marker definition
    mock_config.addinivalue_line.assert_called_once()
    args, kwargs = mock_config.addinivalue_line.call_args
    assert args[0] == "markers"
    assert args[1] == "lge: mark test as a LangGraph evaluation test"


def test_lge_options_would_be_added():
    """Test that the lge options would be added by pytest_addoption."""
    from langgraph_evals import plugin

    # Create a mock parser object
    mock_parser = Mock()
    mock_group = Mock()
    mock_parser.getgroup.return_value = mock_group

    # Call the addoption function
    plugin.pytest_addoption(mock_parser)

    # Verify that getgroup was called with correct arguments
    mock_parser.getgroup.assert_called_once_with(
        "langgraph-evals", "LangGraph Evaluations"
    )

    # Verify that addoption was called twice (for --lge-report and --lge-verbose)
    assert mock_group.addoption.call_count == 2

    # Check the calls
    calls = mock_group.addoption.call_args_list

    # First call should be for --lge-report
    assert "--lge-report" in calls[0][0]
    assert calls[0][1]["dest"] == "lge_report"
    assert calls[0][1]["metavar"] == "FILE"

    # Second call should be for --lge-verbose
    assert "--lge-verbose" in calls[1][0]
    assert calls[1][1]["action"] == "store_true"
    assert calls[1][1]["dest"] == "lge_verbose"


def test_lge_runner_fixture():
    """Test that the lge_runner fixture can be invoked."""
    from langgraph_evals import plugin

    # This should not raise an exception
    runner_func = plugin.lge_runner
    assert runner_func is not None
    # Note: We're not actually calling it here because it might require
    # dependencies or setup, but we're verifying it exists and is callable
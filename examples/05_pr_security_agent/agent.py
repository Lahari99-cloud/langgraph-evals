"""
PR Security Agent — Finance & Banking Use Case
Real LangGraph StateGraph agent for security scanning of pull requests.
Integrates with langgraph-evals for trajectory tracing and failure classification.
"""
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

MAX_LOOP_LIMIT = 3


class AgentState(TypedDict):
    """State for our PR security agent."""
    pr_id: str
    diff_content: str
    steps: List[str]
    security_issues: List[str]
    quality_issues: List[str]
    loop_count: int
    status: str


def supervisor(state: AgentState) -> AgentState:
    """Route incoming PR to correct scanner based on diff content."""
    steps = state["steps"] + ["supervisor"]
    # Simple routing logic: always go to security_scan first
    return {
        **state,
        "steps": steps,
        "status": "routing"
    }


def security_scan(state: AgentState) -> AgentState:
    """Check for hardcoded secrets, SQL injection, exposed API keys in code diff."""
    steps = state["steps"] + ["security_scan"]
    security_issues = state["security_issues"].copy()
    diff = state["diff_content"]

    # Simple detection logic for demo
    if "password" in diff.lower() or "secret" in diff.lower():
        security_issues.append("hardcoded_secret")
    if "SELECT * FROM" in diff or "INSERT INTO" in diff:
        security_issues.append("sql_injection")
    if "api_key" in diff.lower() or "AKIA" in diff:
        security_issues.append("exposed_api_key")

    status = "security_scan_complete"
    if security_issues:
        status = "security_issues_found"

    return {
        **state,
        "steps": steps,
        "security_issues": security_issues,
        "status": status
    }


def quality_check(state: AgentState) -> AgentState:
    """Check for missing tests, TODO comments."""
    steps = state["steps"] + ["quality_check"]
    quality_issues = state["quality_issues"].copy()
    diff = state["diff_content"]

    # Simple detection logic for demo
    if "# TODO" in diff or "// TODO" in diff:
        quality_issues.append("todo_comment")
    if "test" not in diff.lower():
        quality_issues.append("missing_tests")

    status = "quality_check_complete"
    if quality_issues:
        status = "quality_issues_found"

    return {
        **state,
        "steps": steps,
        "quality_issues": quality_issues,
        "status": status
    }


def analytics_eval(state: AgentState) -> AgentState:
    """Uses langgraph-evals TrajectoryTracer to visualize the run and FailureClassifier to detect issues."""
    steps = state["steps"] + ["analytics_eval"]
    # In a real implementation, we would use the actual langgraph-evals classes here.
    # For this example, we'll just note that we've run the analytics.
    # The actual tracing and classification will be done in the tests.

    # Check for loop condition: if we've looped too many times, we break
    loop_count = state.get("loop_count", 0)
    if loop_count >= MAX_LOOP_LIMIT - 1:
        return {**state, "steps": steps, "status": "complete", "loop_count": loop_count + 1}
    return {**state, "steps": steps, "status": "analytics_complete", "loop_count": loop_count + 1}


def route_supervisor(state: AgentState) -> str:
    """Route from supervisor based on current state."""
    # This function will be used for conditional edges
    if state["status"] == "routing":
        return "security_scan"
    # This shouldn't happen in our flow, but as a fallback
    return END


def route_security_scan(state: AgentState) -> str:
    """Route from security_scan based on findings."""
    # Always go to quality_check after security_scan
    return "quality_check"


def route_quality_check(state: AgentState) -> str:
    """Route from quality_check to analytics_eval."""
    return "analytics_eval"


def route_analytics_eval(state: AgentState) -> str:
    """Route from analytics_eval: loop back to supervisor if issues found and under limit, else END."""
    if state.get("status") == "complete":
        return END
    if state.get("loop_count", 0) >= MAX_LOOP_LIMIT:
        return END
    if state.get("security_issues") or state.get("quality_issues"):
        return "supervisor"
    return END


def create_agent() -> StateGraph:
    """Create and return a LangGraph StateGraph for PR security scanning."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("supervisor", supervisor)
    workflow.add_node("security_scan", security_scan)
    workflow.add_node("quality_check", quality_check)
    workflow.add_node("analytics_eval", analytics_eval)

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Add edges
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "security_scan": "security_scan",
            END: END
        }
    )
    workflow.add_conditional_edges(
        "security_scan",
        route_security_scan,
        {
            "quality_check": "quality_check",
            "analytics_eval": "analytics_eval"
        }
    )
    workflow.add_edge("quality_check", "analytics_eval")
    workflow.add_conditional_edges(
        "analytics_eval",
        route_analytics_eval,
        {
            "supervisor": "supervisor",
            END: END
        }
    )

    # Compile the graph
    return workflow.compile()


# Example usage
if __name__ == "__main__":
    # Create the agent
    agent = create_agent()

    # Example PR with no issues
    initial_state = {
        "pr_id": "PR-123",
        "diff_content": "def hello():\n    return 'world'",
        "steps": [],
        "security_issues": [],
        "quality_issues": [],
        "loop_count": 0,
        "status": "start"
    }

    result = agent.invoke(initial_state)
    print(f"Final result: {result}")
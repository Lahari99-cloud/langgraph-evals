"""
Example showing how to use the TrajectoryScorer.
"""

from langgraph_evals.core.trajectory import TrajectoryScorer


def main():
    # Example 1: Efficient trajectory
    print("=== Example 1: Efficient trajectory ===")
    efficient_nodes = ['start', 'fetch_data', 'process_data', 'save_results', 'end']

    scorer = TrajectoryScorer()
    report = scorer.score(efficient_nodes, expected_end_node='end')

    print(f"Efficiency Score: {report.efficiency_score:.2f}")
    print(f"Completion Score: {report.completion_score:.2f}")
    print(f"Loops Detected: {report.loops_detected}")
    print(f"Dead End Detected: {report.dead_end_detected}")
    print(f"Expected End: {report.expected_end_node}")
    print(f"Actual End: {report.actual_end_node}")
    print(f"Explanation: {report.explanation}")
    print()

    # Example 2: Trajectory with loops (using default threshold of 2, so need 3+ visits)
    print("=== Example 2: Trajectory with loops ===")
    looped_nodes = [
        'start', 'fetch_data', 'process_data',
        'fetch_data',  # 2nd visit
        'process_data',
        'fetch_data',  # 3rd visit - should be loop
        'process_data',
        'save_results', 'end'
    ]

    report2 = scorer.score(looped_nodes, expected_end_node='end')

    print(f"Efficiency Score: {report2.efficiency_score:.2f}")
    print(f"Completion Score: {report2.completion_score:.2f}")
    print(f"Loops Detected: {report2.loops_detected}")
    print(f"Dead End Detected: {report2.dead_end_detected}")
    print(f"Expected End: {report2.expected_end_node}")
    print(f"Actual End: {report2.actual_end_node}")
    print(f"Explanation: {report2.explanation}")
    print()

    # Example 3: Using custom loop threshold
    print("=== Example 3: Custom loop threshold (1 visit allowed) ===")
    scorer_strict = TrajectoryScorer()  # max_loops parameter is in score() method

    moderate_loop_nodes = [
        'start', 'fetch_data', 'process_data',
        'fetch_data',  # 2nd visit - loop with threshold=1
        'process_data',
        'save_results', 'end'
    ]

    report3 = scorer_strict.score(moderate_loop_nodes, expected_end_node='end', max_loops=1)

    print(f"Efficiency Score: {report3.efficiency_score:.2f}")
    print(f"Completion Score: {report3.completion_score:.2f}")
    print(f"Loops Detected: {report3.loops_detected}")
    print(f"Dead End Detected: {report3.dead_end_detected}")
    print(f"Expected End: {report3.expected_end_node}")
    print(f"Actual End: {report3.actual_end_node}")
    print(f"Explanation: {report3.explanation}")
    print()

    # Example 4: Trajectory that doesn't reach expected end
    print("=== Example 4: Trajectory that doesn't reach expected end ===")
    incomplete_nodes = ['start', 'fetch_data', 'process_data']
    # Never reaches save_results or end

    report4 = scorer.score(incomplete_nodes, expected_end_node='end')

    print(f"Efficiency Score: {report4.efficiency_score:.2f}")
    print(f"Completion Score: {report4.completion_score:.2f}")
    print(f"Loops Detected: {report4.loops_detected}")
    print(f"Dead End Detected: {report4.dead_end_detected}")
    print(f"Expected End: {report4.expected_end_node}")
    print(f"Actual End: {report4.actual_end_node}")
    print(f"Explanation: {report4.explanation}")


if __name__ == "__main__":
    main()
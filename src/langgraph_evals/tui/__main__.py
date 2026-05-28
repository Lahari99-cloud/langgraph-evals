"""
Entry point for running langgraph_evals.tui as a module.
"""
import sys
from .cli import main

if __name__ == "__main__":
    # If no arguments, show help? But we expect 'demo'
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Remove the 'demo' argument so cli.main doesn't see it
        sys.argv.pop(1)
    sys.exit(main())
# Contributing to langgraph-evals

Thank you for considering contributing to langgraph-evals! We welcome contributions from the community.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your feature or fix
4. **Make your changes**
5. **Add tests** for new functionality
6. **Ensure all tests pass**
7. **Submit a pull request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/langgraph-evals.git
cd langgraph-evals

# Install in development mode
pip install -e .[dev]

# Run the test suite
pytest

# Run tests with coverage
pytest --cov=src/langgraph_evals
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

To check formatting:
```bash
black --check src/
ruff check src/
mypy src/
```

To automatically format:
```bash
black src/
ruff check --fix src/
```

## Adding New Features

When adding new features:
1. Add corresponding tests in the `tests/` directory
2. Update the documentation if needed
3. Follow the existing code patterns and style
4. Ensure backward compatibility

## Reporting Issues

Please use the GitHub issue tracker to report bugs or request features. Include:
- Clear description of the issue
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
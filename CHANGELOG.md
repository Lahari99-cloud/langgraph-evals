# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Real LangGraph integration with `GraphRunCapture` context manager
- TUI Trajectory Tracer with Rich-based terminal visualization
- CLI demo command: `lge-trace demo`
- CONTRIBUTING.md file
- Enhanced pytest plugin with better trace collection
- Comprehensive docstrings and examples

### Changed
- Updated assertions.py to handle both dict and object-based graph run data
- Improved Travis CI workflow with Node.js 24 compatibility
- Updated README with new sections and badges
- Refactored TUI components for better separation of concerns

### Fixed
- Windows compatibility issues with Unicode characters in TUI
- Test isolation and proper cleanup in LangGraph integration tests
- Cookiecutter template issues in example projects
- Various minor bugs in failure classification logic

## [0.1.0] - 2026-05-28
### Added
- Initial release with core assertion utilities (6 functions)
- TrajectoryScorer class with efficiency and completion scoring
- Memory persistence testing functions (3 assertion functions)
- Failure taxonomy classifier with 7 failure types
- Pytest plugin with `lge` marker, CLI flags, and fixture
- Console and JSON reporters
- Three comprehensive examples:
  - Simple agent demonstration
  - Multi-agent memory isolation testing
  - Regulated/CI environment example with zero external dependencies
- Windows compatibility fixes
- Foundational documentation and setup

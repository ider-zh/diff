"""
CONTRIBUTING Guide for deep-diff
================================

Thank you for considering contributing to deep-diff! This document provides
guidelines and instructions for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/diff.git
   cd diff
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** to the code
3. **Write or update tests** for your changes
4. **Run tests locally**:
   ```bash
   pytest
   ```
5. **Format and lint your code**:
   ```bash
   black deep_diff tests
   ruff check --fix deep_diff tests
   mypy deep_diff
   ```

### Testing

- All new features should include tests
- Tests should be added to `tests/test_deep_diff.py`
- Aim for >90% code coverage
- Run tests with coverage:
  ```bash
  pytest --cov=deep_diff --cov-report=html
  ```

### Code Style

- **Formatting**: Use `black` (line length: 100)
- **Linting**: Use `ruff`
- **Type hints**: Add type hints to all public functions
- **Docstrings**: Use Google-style docstrings

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues when applicable: "Fix #123"
- Example: "Add type hints to diff function"

### Pull Request Process

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
2. **Create a Pull Request** on GitHub
3. **Write a clear PR description**:
   - What changes you made
   - Why you made them
   - Any related issues
4. **Ensure CI passes** (tests, linting, type checking)
5. **Request review** from maintainers

## Areas for Contribution

- 🐛 **Bug fixes**: Report and fix issues
- ✨ **Features**: Suggest and implement new functionality
- 📚 **Documentation**: Improve documentation and examples
- 🧪 **Tests**: Add test cases for edge cases
- 🚀 **Performance**: Optimize performance-critical code

## Reporting Issues

- Use GitHub Issues for bug reports
- Include:
  - Clear description of the issue
  - Steps to reproduce
  - Expected vs actual behavior
  - Python version and OS
  - Minimal code example

## Questions?

- Open an issue for discussion
- Check existing issues and PRs first
- Be respectful and constructive

## Code of Conduct

- Be respectful to all contributors
- Follow PEP 8 style guidelines
- Test your changes thoroughly
- Write clear, understandable code

## License

By contributing, you agree that your contributions will be licensed under
the same BSD 3-Clause License as the project.

---

Thanks for contributing to deep-diff! 🎉
"""

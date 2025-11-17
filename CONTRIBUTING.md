# Contributing to BitDubber

First off, thank you for considering contributing to BitDubber! It's people like you that make BitDubber such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by respect, professionalism, and inclusivity. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what you expected**
* **Include screenshots if possible**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Provide specific examples to demonstrate the enhancement**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

1. **Fork and clone the repository**:
```bash
git clone https://github.com/your-username/BitDubber.git
cd BitDubber
```

2. **Install uv package manager**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Install development dependencies**:
```bash
make install-dev
```

4. **Create a branch**:
```bash
git checkout -b feature/your-feature-name
```

## Code Style

### Python Style Guide

* Follow PEP 8 style guidelines
* Use type hints for all function signatures
* Write comprehensive docstrings (Google style)
* Maximum line length: 100 characters
* Use meaningful variable and function names

### Running Code Quality Checks

```bash
# Format code
make format

# Run linter
make lint

# Run type checker
make type-check

# Run all checks
make check-all
```

## Testing

### Writing Tests

* Write tests for all new features
* Ensure existing tests pass
* Aim for >80% code coverage
* Use pytest fixtures for common setups
* Mock external dependencies

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add voice command for window management

- Implement window minimize/maximize commands
- Add tests for window operations
- Update documentation with new commands

Fixes #123
```

## Documentation

* Update README.md if you change functionality
* Add docstrings to new functions and classes
* Update type hints when changing function signatures
* Keep documentation clear and concise

## Review Process

1. **Self-review**: Review your own code first
2. **Automated checks**: Ensure all CI checks pass
3. **Peer review**: Wait for maintainer review
4. **Address feedback**: Make requested changes
5. **Merge**: Maintainer will merge when approved

## Community

* Be respectful and constructive
* Help others when you can
* Share your knowledge
* Have fun! 🎉

## Questions?

Feel free to open an issue with the "question" label or contact the maintainer at contact@ruslanmv.com.

---

**Thank you for contributing to BitDubber!** 🤖

*Author: Ruslan Magana*
*Website: ruslanmv.com*

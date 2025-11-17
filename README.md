# BitDubber

**A Cutting-Edge Desktop Assistant with Screen Reading and Voice Command Capabilities**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linter-ruff-red)](https://github.com/astral-sh/ruff)

---

## About

**BitDubber** is a revolutionary desktop assistant that combines advanced screen-reading capabilities with intelligent voice command recognition. By understanding the context of your screen and responding to natural voice commands, BitDubber transforms how you interact with your computer—making complex workflows effortless and accessible to everyone.

Whether you're navigating applications, automating repetitive tasks, or need enhanced accessibility features, BitDubber is your intelligent companion for a more productive desktop experience.

**Author:** [Ruslan Magana](https://ruslanmv.com)
**License:** Apache 2.0
**Website:** [ruslanmv.com](https://ruslanmv.com)

---

## Features

- **Intelligent Screen Reading**: Automatically captures and analyzes your desktop screen using advanced OCR technology
- **Voice Command Recognition**: Execute tasks effortlessly with natural voice commands
- **Context-Aware Actions**: Intelligently adapts to your active applications and workflows
- **Modular Architecture**: Clean, extensible codebase following industry best practices
- **Comprehensive Testing**: Full test coverage with unit and integration tests
- **Type-Safe**: Complete type hints throughout the codebase for better IDE support
- **Privacy-Focused**: All processing designed with user security and privacy as top priorities
- **Professional CLI**: Rich command-line interface with intuitive commands
- **Extensible**: Easy to extend with custom actions and integrations

---

## Installation

### Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Tesseract OCR engine
- PyAudio dependencies

### System Dependencies

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr python3-pyaudio portaudio19-dev
```

#### macOS
```bash
brew install tesseract portaudio
```

#### Windows
Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and ensure it's in your PATH.

### Install BitDubber

#### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/ruslanmv/BitDubber.git
cd BitDubber

# Install with uv
make install

# For development installation with all tools
make install-dev
```

#### Using pip

```bash
pip install -e .

# For development
pip install -e ".[dev,test,docs]"
```

---

## Usage

### Quick Start

```bash
# Display information about BitDubber
bitdubber info

# Test screen reading functionality
bitdubber screen-test

# Test voice recognition
bitdubber voice-test

# Run BitDubber in interactive mode
bitdubber run
```

### Interactive Mode

In interactive mode, BitDubber listens continuously for voice commands:

```bash
bitdubber run
```

**Example Commands:**
- "open browser"
- "search python documentation"
- "open calculator"
- "open settings"
- "stop listening" (to exit)

### Python API

You can also use BitDubber as a Python library:

```python
from bitdubber import ScreenReader, VoiceRecognizer, ActionExecutor

# Initialize components
screen_reader = ScreenReader()
voice_recognizer = VoiceRecognizer()
action_executor = ActionExecutor()

# Capture and read screen
text = screen_reader.capture_and_read()
print(f"Screen text: {text}")

# Listen for voice command
voice_recognizer.initialize_microphone()
command = voice_recognizer.listen_for_command()
print(f"Command: {command}")

# Execute action
parsed = voice_recognizer.parse_command(command)
result = action_executor.execute_action(
    parsed["action"],
    parsed["target"]
)
print(f"Result: {result}")
```

---

## Configuration

BitDubber can be configured using environment variables or a `.env` file:

```bash
# Application settings
BITDUBBER_DEBUG=false
BITDUBBER_LOG_LEVEL=INFO

# Screen capture settings
BITDUBBER_SCREENSHOT_DIR=screenshots
BITDUBBER_SCREENSHOT_INTERVAL=1.0

# OCR settings
BITDUBBER_OCR_LANGUAGE=eng
BITDUBBER_OCR_CONFIDENCE_THRESHOLD=60.0

# Voice recognition settings
BITDUBBER_VOICE_LANGUAGE=en-US
BITDUBBER_VOICE_TIMEOUT=5.0
BITDUBBER_VOICE_ENERGY_THRESHOLD=300

# Action execution settings
BITDUBBER_ACTION_TIMEOUT=30.0
```

---

## Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Run code formatting
make format

# Run linting
make lint

# Run type checking
make type-check

# Run all quality checks
make quality
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run tests with verbose output
make test-verbose
```

### Project Structure

```
BitDubber/
├── src/bitdubber/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Entry point for python -m bitdubber
│   ├── cli.py              # Command-line interface
│   ├── config/             # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py     # Application settings
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   ├── screen_reader.py      # Screen capture & OCR
│   │   ├── voice_recognizer.py   # Voice recognition
│   │   └── action_executor.py    # Action execution
│   └── utils/              # Utility modules
│       ├── __init__.py
│       ├── exceptions.py   # Custom exceptions
│       └── logger.py       # Logging configuration
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_screen_reader.py
│   ├── test_voice_recognizer.py
│   ├── test_action_executor.py
│   ├── test_config.py
│   └── test_exceptions.py
├── pyproject.toml          # Project metadata & dependencies
├── Makefile                # Development automation
├── LICENSE                 # Apache 2.0 license
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

---

## Makefile Commands

BitDubber includes a comprehensive Makefile for development automation:

```bash
# Installation
make install          # Install production dependencies
make install-dev      # Install development dependencies
make sync             # Sync dependencies with uv

# Code Quality
make format           # Format code with black
make format-check     # Check code formatting
make lint             # Run ruff linter
make lint-fix         # Run ruff with auto-fix
make type-check       # Run mypy type checker
make quality          # Run all quality checks

# Testing
make test             # Run all tests
make test-cov         # Run tests with coverage
make test-unit        # Run unit tests only
make test-integration # Run integration tests
make test-verbose     # Run tests with verbose output

# Build & Distribution
make build            # Build distribution packages
make dist             # Alias for build

# Documentation
make docs             # Build documentation
make serve-docs       # Serve documentation locally

# Development
make pre-commit       # Run pre-commit hooks
make run              # Run BitDubber
make dev              # Setup development environment

# Cleanup
make clean            # Clean build artifacts
make clean-all        # Clean all generated files

# CI/CD
make ci-test          # Run tests for CI/CD
make ci-lint          # Run linting for CI/CD
make ci               # Run all CI checks

# Help
make help             # Display all available commands
```

---

## Use Cases

### Effortless Navigation
Quickly switch between apps, tabs, and documents with simple voice commands.

### Productivity Boost
Automate repetitive tasks and workflows to save time and reduce manual effort.

### Accessibility
Empower users with disabilities to interact with their desktop in a more inclusive way.

### Entertainment
Manage media playback and streaming platforms without lifting a finger.

### Custom Workflows
Extend BitDubber with custom actions tailored to your specific needs.

---

## Architecture

BitDubber follows a modular architecture with clear separation of concerns:

- **Config Layer**: Manages application settings with validation using Pydantic
- **Core Layer**: Contains the main business logic (screen reading, voice recognition, action execution)
- **Utils Layer**: Provides shared utilities (logging, exceptions)
- **CLI Layer**: Presents a rich command-line interface using Click and Rich

All modules include:
- Comprehensive docstrings (Google style)
- Type hints for all functions and methods
- Proper error handling with custom exceptions
- Extensive unit and integration tests

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Workflow

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run quality checks (`make quality`)
5. Run tests (`make test`)
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

---

## Testing

BitDubber includes comprehensive test coverage:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Mocked Dependencies**: External dependencies are properly mocked
- **Coverage Reports**: Detailed coverage reports with HTML output

Run tests with:
```bash
make test-cov
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Roadmap

- [ ] Enhanced NLP for more natural command parsing
- [ ] GUI application with system tray integration
- [ ] Plugin system for custom actions
- [ ] Multi-monitor support
- [ ] Cloud synchronization for settings
- [ ] Machine learning for personalized workflows
- [ ] Integration with popular applications (Spotify, Slack, etc.)
- [ ] Mobile companion app
- [ ] Multi-language support

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

```
Copyright 2024 Ruslan Magana

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## Acknowledgments

- **Tesseract OCR**: For powerful open-source OCR capabilities
- **Google Speech Recognition**: For reliable voice recognition
- **Python Community**: For excellent libraries and tools
- **Contributors**: Thank you to all contributors who help make BitDubber better

---

## Support & Contact

- **Website**: [ruslanmv.com](https://ruslanmv.com)
- **Issues**: [GitHub Issues](https://github.com/ruslanmv/BitDubber/issues)
- **Email**: contact@ruslanmv.com

---

## Security

If you discover a security vulnerability, please send an email to contact@ruslanmv.com. All security vulnerabilities will be promptly addressed.

---

<div align="center">

**BitDubber** - Transforming How You Work with Your Desktop

Made with ❤️ by [Ruslan Magana](https://ruslanmv.com)

</div>

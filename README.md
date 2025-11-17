# 🤖 BitDubber - AI-Powered Desktop Assistant

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**BitDubber** is an intelligent desktop assistant that combines voice commands with advanced AI vision to automate UI interactions. Using IBM Watson's Speech services and Meta's LLaMA models, BitDubber can understand your voice commands, analyze your screen, and execute complex automation tasks.

---

## ✨ Features

- **🎤 Voice Command Recognition**: Convert speech to text using IBM Watson Speech-to-Text
- **🖼️ Screen Analysis**: Capture and analyze UI elements using LLaMA 3.2 Vision model
- **🤖 Intelligent Action Planning**: Determine optimal action sequences with LLaMA 3.1
- **⚡ Automated Execution**: Execute mouse clicks, keyboard inputs, and complex workflows
- **🔊 Voice Feedback**: Hear planned actions through IBM Watson Text-to-Speech
- **🎨 User-Friendly Interface**: Interactive Gradio web interface for easy interaction
- **🛡️ Production-Ready**: Comprehensive error handling, logging, and type safety
- **📦 Modern Python**: Built with PEP 8 compliance, type hints, and best practices

---

## 📋 Table of Contents

- [About](#about)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 📖 About

BitDubber bridges the gap between natural voice commands and desktop automation. By leveraging state-of-the-art AI models, it provides an intuitive way to control your computer through voice, making complex tasks accessible and efficient.

### How It Works

1. **Voice Input**: Speak your command through the microphone
2. **Speech Recognition**: IBM Watson STT converts your speech to text
3. **Screen Capture**: Automatic screenshot of your current screen
4. **UI Analysis**: LLaMA 3.2 Vision identifies clickable elements
5. **Action Planning**: LLaMA 3.1 determines the sequence of actions
6. **Confirmation**: Voice feedback describes planned actions
7. **Execution**: Automated execution of the action sequence

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- IBM Cloud account with Watson services
- IBM WatsonX access for LLaMA models

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/ruslanmv/BitDubber.git
cd BitDubber
```

2. **Install uv package manager** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Install dependencies**:
```bash
make install-dev
```

Or manually with uv:
```bash
uv sync
```

4. **Configure environment variables** (see [Configuration](#configuration))

5. **Run the application**:
```bash
make run
```

---

## ⚙️ Configuration

Create a `.env` file in the project root with your IBM Cloud credentials:

```env
# IBM Watson Speech-to-Text
STT_API_KEY=your_speech_to_text_api_key
STT_URL=your_speech_to_text_service_url

# IBM Watson Text-to-Speech
TTS_API_KEY=your_text_to_speech_api_key
TTS_URL=your_text_to_speech_service_url

# IBM WatsonX (LLaMA Models)
WATSONX_APIKEY=your_watsonx_api_key
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
PROJECT_ID=your_project_id
```

### Getting IBM Cloud Credentials

1. **Create an IBM Cloud account**: [cloud.ibm.com](https://cloud.ibm.com/)
2. **Create Speech-to-Text service**: Navigate to Catalog → AI → Speech to Text
3. **Create Text-to-Speech service**: Navigate to Catalog → AI → Text to Speech
4. **Create WatsonX project**: Navigate to IBM WatsonX → Create Project
5. **Retrieve credentials**: Go to Service Credentials in each service dashboard

---

## 💻 Usage

### Command Line

Run the application using make:
```bash
make run
```

Or directly with Python:
```bash
python -m bitdubber.app
```

Or using the installed command:
```bash
bitdubber
```

### Web Interface

1. Launch the application
2. Open the provided URL in your browser (typically `http://127.0.0.1:7860`)
3. Click the microphone button and speak your command
4. Watch as BitDubber analyzes and executes your request

### Example Commands

- "Open Wikipedia"
- "Search for artificial intelligence"
- "Click the menu button"
- "Type hello world and press enter"

---

## 🏗️ Architecture

### Project Structure

```
BitDubber/
├── bitdubber/              # Main package
│   ├── __init__.py         # Package initialization
│   └── app.py              # Core application logic
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_watson.py
│   └── test_automation.py
├── backup/                 # Version history
├── tools/                  # Utility scripts
├── .env                    # Environment variables (create this)
├── .gitignore              # Git ignore rules
├── LICENSE                 # Apache 2.0 license
├── Makefile                # Build automation
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### Core Components

- **BitDubberConfig**: Environment configuration manager
- **WatsonServices**: IBM Watson STT/TTS wrapper
- **LLaMAService**: IBM WatsonX LLaMA integration
- **ScreenAutomation**: UI automation and screenshot handling
- **BitDubberApp**: Main application orchestrator

---

## 🛠️ Development

### Setup Development Environment

```bash
make install-dev
```

### Code Quality

Run all quality checks:
```bash
make check-all
```

Individual checks:
```bash
make lint          # Run ruff linter
make format        # Format with black and isort
make type-check    # Run mypy type checker
```

### Available Make Commands

Run `make help` to see all available commands:

```bash
make help          # Show all available commands
make install       # Install production dependencies
make install-dev   # Install development dependencies
make clean         # Remove build artifacts
make lint          # Run linter
make format        # Format code
make test          # Run tests
make test-cov      # Run tests with coverage
make build         # Build distribution packages
```

---

## 🧪 Testing

### Run Tests

```bash
make test
```

### Run Tests with Coverage

```bash
make test-cov
```

Coverage reports will be generated in `htmlcov/` directory.

### Test Structure

- `test_app.py`: Application orchestration tests
- `test_watson.py`: Watson services integration tests
- `test_automation.py`: UI automation tests

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following PEP 8 and project conventions
4. Run tests and quality checks (`make check-all test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings (Google style)
- Maintain test coverage above 80%
- Use meaningful variable and function names

---

## 📝 License

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

## 👤 Author

**Ruslan Magana**

- Website: [ruslanmv.com](https://ruslanmv.com)
- GitHub: [@ruslanmv](https://github.com/ruslanmv)
- Email: contact@ruslanmv.com

---

## 🙏 Acknowledgments

- **IBM Watson** for Speech-to-Text and Text-to-Speech services
- **Meta AI** for LLaMA models
- **Gradio** for the amazing web interface framework
- The open-source community for excellent tools and libraries

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Custom voice models training
- [ ] Advanced workflow recording and playback
- [ ] Cross-platform support (macOS, Linux)
- [ ] Plugin system for extensibility
- [ ] Real-time action visualization
- [ ] Voice authentication and security features

---

## 📊 Project Status

**Status**: Beta - Ready for testing and feedback

**Version**: 1.0.0

**Last Updated**: 2024

---

## 📚 Documentation

For more detailed documentation, see:

- [Setup Guide](setup.md) - Detailed installation instructions
- [API Documentation](#) - Coming soon
- [User Guide](#) - Coming soon

---

## ⚠️ Disclaimer

BitDubber automates UI interactions on your computer. Use responsibly and ensure you have proper permissions before automating tasks on any system. The authors are not responsible for misuse or damages resulting from the use of this software.

---

<div align="center">

**Built with ❤️ by Ruslan Magana**

[⬆ Back to Top](#-bitdubber---ai-powered-desktop-assistant)

</div>

.PHONY: help install install-dev clean lint format type-check test test-cov run dev build check-all

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Python and UV settings
PYTHON := python3
UV := uv
SRC_DIR := bitdubber
TEST_DIR := tests

##@ General

help: ## Display this help message
	@echo "$(BLUE)BitDubber - AI-Powered Desktop Assistant$(NC)"
	@echo "$(GREEN)Author: Ruslan Magana | Website: ruslanmv.com$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(YELLOW)<target>$(NC)\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup & Installation

install: ## Install production dependencies using uv
	@echo "$(GREEN)Installing production dependencies with uv...$(NC)"
	$(UV) sync --no-dev
	@echo "$(GREEN)✓ Installation complete!$(NC)"

install-dev: ## Install all dependencies including dev tools using uv
	@echo "$(GREEN)Installing all dependencies (including dev) with uv...$(NC)"
	$(UV) sync
	@echo "$(GREEN)✓ Development environment ready!$(NC)"

setup: install-dev ## Complete setup for development (alias for install-dev)
	@echo "$(GREEN)✓ Development environment fully configured!$(NC)"

##@ Code Quality

lint: ## Run ruff linter on the codebase
	@echo "$(BLUE)Running ruff linter...$(NC)"
	$(UV) run ruff check $(SRC_DIR) $(TEST_DIR) --fix
	@echo "$(GREEN)✓ Linting complete!$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code with black...$(NC)"
	$(UV) run black $(SRC_DIR) $(TEST_DIR)
	@echo "$(BLUE)Sorting imports with isort...$(NC)"
	$(UV) run isort $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Code formatting complete!$(NC)"

format-check: ## Check code formatting without making changes
	@echo "$(BLUE)Checking code format...$(NC)"
	$(UV) run black --check $(SRC_DIR) $(TEST_DIR)
	$(UV) run isort --check-only $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Format check complete!$(NC)"

type-check: ## Run mypy type checker
	@echo "$(BLUE)Running type checks with mypy...$(NC)"
	$(UV) run mypy $(SRC_DIR)
	@echo "$(GREEN)✓ Type checking complete!$(NC)"

check-all: lint format-check type-check ## Run all code quality checks
	@echo "$(GREEN)✓ All quality checks passed!$(NC)"

##@ Testing

test: ## Run tests with pytest
	@echo "$(BLUE)Running tests...$(NC)"
	$(UV) run pytest $(TEST_DIR) -v
	@echo "$(GREEN)✓ Tests complete!$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(UV) run pytest $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	$(UV) run pytest-watch $(TEST_DIR)

##@ Development

run: ## Run the BitDubber application
	@echo "$(BLUE)Starting BitDubber...$(NC)"
	$(UV) run $(PYTHON) -m $(SRC_DIR).app

dev: ## Run the application in development mode
	@echo "$(BLUE)Starting BitDubber in development mode...$(NC)"
	$(UV) run $(PYTHON) -m $(SRC_DIR).app

##@ Build & Distribution

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(UV) build
	@echo "$(GREEN)✓ Build complete! Packages in dist/$(NC)"

publish-test: build ## Publish to TestPyPI
	@echo "$(BLUE)Publishing to TestPyPI...$(NC)"
	$(UV) publish --repository testpypi
	@echo "$(GREEN)✓ Published to TestPyPI!$(NC)"

publish: build ## Publish to PyPI
	@echo "$(YELLOW)Publishing to PyPI...$(NC)"
	$(UV) publish
	@echo "$(GREEN)✓ Published to PyPI!$(NC)"

##@ Cleaning

clean: ## Remove build artifacts and cache files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -f ui_elements.csv
	rm -f screenshot.png
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-all: clean ## Remove all generated files including virtual environment
	@echo "$(YELLOW)Removing virtual environment...$(NC)"
	rm -rf .venv/
	@echo "$(GREEN)✓ Complete cleanup done!$(NC)"

##@ Utilities

env-check: ## Check environment variables are configured
	@echo "$(BLUE)Checking environment configuration...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)✗ .env file not found!$(NC)"; \
		echo "$(YELLOW)Please create .env file with required credentials$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Environment configured!$(NC)"

version: ## Show version information
	@echo "$(BLUE)BitDubber Version Information$(NC)"
	@echo "Version: $$(grep '^version' pyproject.toml | cut -d'"' -f2)"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "UV: $$($(UV) --version)"

info: ## Display project information
	@echo "$(BLUE)╔════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║         BitDubber - Production Ready          ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Project:$(NC) AI-Powered Desktop Assistant"
	@echo "$(GREEN)Author:$(NC)  Ruslan Magana"
	@echo "$(GREEN)Website:$(NC) ruslanmv.com"
	@echo "$(GREEN)License:$(NC) Apache 2.0"
	@echo "$(GREEN)Version:$(NC) $$(grep '^version' pyproject.toml | cut -d'"' -f2)"
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  1. Run 'make install-dev' to setup"
	@echo "  2. Create .env file with credentials"
	@echo "  3. Run 'make run' to start"
	@echo ""
	@echo "$(YELLOW)Documentation:$(NC) See README.md"

##@ CI/CD

ci: install-dev check-all test-cov ## Run full CI pipeline
	@echo "$(GREEN)✓ CI pipeline completed successfully!$(NC)"

pre-commit: format lint type-check test ## Run pre-commit checks
	@echo "$(GREEN)✓ Pre-commit checks passed!$(NC)"

.PHONY: help install install-dev clean lint format type-check test test-cov test-unit test-integration build docs serve-docs pre-commit run

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)BitDubber - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install production dependencies using uv
	@echo "$(GREEN)Installing production dependencies with uv...$(NC)"
	uv pip install -e .

install-dev: ## Install development dependencies using uv
	@echo "$(GREEN)Installing development dependencies with uv...$(NC)"
	uv pip install -e ".[dev,test,docs]"
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	pre-commit install

sync: ## Sync dependencies using uv
	@echo "$(GREEN)Syncing dependencies with uv...$(NC)"
	uv sync

##@ Code Quality

lint: ## Run ruff linter
	@echo "$(GREEN)Running ruff linter...$(NC)"
	ruff check src/ tests/

lint-fix: ## Run ruff linter with auto-fix
	@echo "$(GREEN)Running ruff linter with auto-fix...$(NC)"
	ruff check --fix src/ tests/

format: ## Format code with black
	@echo "$(GREEN)Formatting code with black...$(NC)"
	black src/ tests/

format-check: ## Check code formatting without modifying
	@echo "$(GREEN)Checking code formatting...$(NC)"
	black --check src/ tests/

type-check: ## Run mypy type checker
	@echo "$(GREEN)Running mypy type checker...$(NC)"
	mypy src/bitdubber

quality: lint format type-check ## Run all quality checks

##@ Testing

test: ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	pytest

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	pytest --cov=bitdubber --cov-report=term-missing --cov-report=html

test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	pytest -m unit

test-integration: ## Run integration tests only
	@echo "$(GREEN)Running integration tests...$(NC)"
	pytest -m integration

test-verbose: ## Run tests with verbose output
	@echo "$(GREEN)Running tests with verbose output...$(NC)"
	pytest -v

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	pytest-watch

##@ Build & Distribution

build: clean ## Build distribution packages
	@echo "$(GREEN)Building distribution packages...$(NC)"
	uv build

dist: build ## Alias for build

##@ Documentation

docs: ## Build documentation
	@echo "$(GREEN)Building documentation...$(NC)"
	mkdocs build

serve-docs: ## Serve documentation locally
	@echo "$(GREEN)Serving documentation at http://127.0.0.1:8000$(NC)"
	mkdocs serve

##@ Development

pre-commit: ## Run pre-commit hooks on all files
	@echo "$(GREEN)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

run: ## Run the BitDubber application
	@echo "$(GREEN)Starting BitDubber...$(NC)"
	python -m bitdubber

dev: install-dev ## Setup development environment
	@echo "$(GREEN)Development environment ready!$(NC)"

##@ Cleanup

clean: ## Clean build artifacts and cache files
	@echo "$(YELLOW)Cleaning build artifacts and cache files...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg" -delete
	@echo "$(GREEN)Clean complete!$(NC)"

clean-all: clean ## Clean all generated files including venv
	@echo "$(YELLOW)Cleaning all generated files...$(NC)"
	rm -rf .venv/
	rm -rf venv/
	@echo "$(GREEN)Deep clean complete!$(NC)"

##@ CI/CD

ci-test: ## Run tests for CI/CD
	@echo "$(GREEN)Running CI tests...$(NC)"
	pytest --cov=bitdubber --cov-report=xml --cov-report=term

ci-lint: ## Run linting for CI/CD
	@echo "$(GREEN)Running CI linting...$(NC)"
	ruff check src/ tests/
	black --check src/ tests/
	mypy src/bitdubber

ci: ci-lint ci-test ## Run all CI checks
	@echo "$(GREEN)All CI checks passed!$(NC)"

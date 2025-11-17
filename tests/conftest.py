"""Pytest configuration and shared fixtures.

This module provides shared fixtures and configuration for all tests.
"""

from pathlib import Path
from typing import Generator

import pytest

from bitdubber.config.settings import Settings


@pytest.fixture
def test_settings(tmp_path: Path) -> Settings:
    """Provide test settings with temporary directories.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        Settings instance configured for testing.
    """
    screenshot_dir = tmp_path / "screenshots"
    log_file = tmp_path / "test.log"

    return Settings(
        debug=True,
        log_level="DEBUG",
        screenshot_dir=screenshot_dir,
        log_file=log_file,
    )


@pytest.fixture
def temp_screenshot_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Provide temporary screenshot directory.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Yields:
        Path to temporary screenshot directory.
    """
    screenshot_dir = tmp_path / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    yield screenshot_dir


@pytest.fixture(autouse=True)
def reset_settings_cache() -> Generator[None, None, None]:
    """Reset settings cache before each test.

    This ensures that each test gets a fresh settings instance.
    """
    from bitdubber.config.settings import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()

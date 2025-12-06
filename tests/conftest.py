"""Pytest configuration and fixtures for BitDubber tests.

Author: Ruslan Magana
Website: ruslanmv.com
"""

import sys
from unittest.mock import MagicMock

import pytest

# Mock pyautogui before any imports to avoid display issues in headless environments
sys.modules["pyautogui"] = MagicMock()
sys.modules["mouseinfo"] = MagicMock()


@pytest.fixture(autouse=True)
def mock_pyautogui():
    """Mock pyautogui for all tests to avoid display dependencies."""
    pyautogui_mock = MagicMock()
    pyautogui_mock.screenshot.return_value = MagicMock()
    pyautogui_mock.moveTo = MagicMock()
    pyautogui_mock.click = MagicMock()
    pyautogui_mock.typewrite = MagicMock()
    pyautogui_mock.press = MagicMock()

    sys.modules["pyautogui"] = pyautogui_mock
    yield pyautogui_mock

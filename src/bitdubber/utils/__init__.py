"""Utility modules for BitDubber.

This package contains utility functions and classes used throughout the application.
"""

from bitdubber.utils.exceptions import (
    ActionExecutionError,
    BitDubberError,
    ConfigurationError,
    ScreenCaptureError,
    VoiceRecognitionError,
)
from bitdubber.utils.logger import get_logger, setup_logging

__all__ = [
    "BitDubberError",
    "ScreenCaptureError",
    "VoiceRecognitionError",
    "ActionExecutionError",
    "ConfigurationError",
    "get_logger",
    "setup_logging",
]

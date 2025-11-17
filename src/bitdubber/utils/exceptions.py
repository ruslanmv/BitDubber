"""Custom exceptions for BitDubber.

This module defines all custom exceptions used throughout the BitDubber application.
"""

from typing import Optional


class BitDubberError(Exception):
    """Base exception for all BitDubber errors.

    All custom exceptions in BitDubber inherit from this base class.
    """

    def __init__(self, message: str, details: Optional[str] = None) -> None:
        """Initialize BitDubberError.

        Args:
            message: The error message.
            details: Optional additional details about the error.
        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the error.

        Returns:
            Formatted error message with optional details.
        """
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class ScreenCaptureError(BitDubberError):
    """Exception raised when screen capture fails.

    This exception is raised when the application cannot capture
    or process the screen content.
    """

    pass


class VoiceRecognitionError(BitDubberError):
    """Exception raised when voice recognition fails.

    This exception is raised when the application cannot recognize
    or process voice input.
    """

    pass


class ActionExecutionError(BitDubberError):
    """Exception raised when action execution fails.

    This exception is raised when the application cannot execute
    the requested action.
    """

    pass


class ConfigurationError(BitDubberError):
    """Exception raised when configuration is invalid.

    This exception is raised when the application configuration
    is missing or invalid.
    """

    pass

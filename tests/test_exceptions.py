"""Unit tests for custom exceptions."""

import pytest

from bitdubber.utils.exceptions import (
    ActionExecutionError,
    BitDubberError,
    ConfigurationError,
    ScreenCaptureError,
    VoiceRecognitionError,
)


class TestExceptions:
    """Test cases for custom exception classes."""

    @pytest.mark.unit
    def test_bitdubber_error_basic(self):
        """Test basic BitDubberError."""
        error = BitDubberError("Test error")

        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details is None

    @pytest.mark.unit
    def test_bitdubber_error_with_details(self):
        """Test BitDubberError with details."""
        error = BitDubberError("Test error", details="Additional information")

        assert "Test error" in str(error)
        assert "Additional information" in str(error)
        assert error.details == "Additional information"

    @pytest.mark.unit
    def test_screen_capture_error(self):
        """Test ScreenCaptureError inheritance."""
        error = ScreenCaptureError("Capture failed")

        assert isinstance(error, BitDubberError)
        assert str(error) == "Capture failed"

    @pytest.mark.unit
    def test_screen_capture_error_with_details(self):
        """Test ScreenCaptureError with details."""
        error = ScreenCaptureError("Capture failed", details="No display found")

        assert "Capture failed" in str(error)
        assert "No display found" in str(error)

    @pytest.mark.unit
    def test_voice_recognition_error(self):
        """Test VoiceRecognitionError inheritance."""
        error = VoiceRecognitionError("Recognition failed")

        assert isinstance(error, BitDubberError)
        assert str(error) == "Recognition failed"

    @pytest.mark.unit
    def test_voice_recognition_error_with_details(self):
        """Test VoiceRecognitionError with details."""
        error = VoiceRecognitionError(
            "Recognition failed", details="No microphone detected"
        )

        assert "Recognition failed" in str(error)
        assert "No microphone detected" in str(error)

    @pytest.mark.unit
    def test_action_execution_error(self):
        """Test ActionExecutionError inheritance."""
        error = ActionExecutionError("Execution failed")

        assert isinstance(error, BitDubberError)
        assert str(error) == "Execution failed"

    @pytest.mark.unit
    def test_action_execution_error_with_details(self):
        """Test ActionExecutionError with details."""
        error = ActionExecutionError(
            "Execution failed", details="Command not found"
        )

        assert "Execution failed" in str(error)
        assert "Command not found" in str(error)

    @pytest.mark.unit
    def test_configuration_error(self):
        """Test ConfigurationError inheritance."""
        error = ConfigurationError("Invalid configuration")

        assert isinstance(error, BitDubberError)
        assert str(error) == "Invalid configuration"

    @pytest.mark.unit
    def test_configuration_error_with_details(self):
        """Test ConfigurationError with details."""
        error = ConfigurationError(
            "Invalid configuration", details="Missing required field"
        )

        assert "Invalid configuration" in str(error)
        assert "Missing required field" in str(error)

    @pytest.mark.unit
    def test_exception_can_be_raised(self):
        """Test that exceptions can be raised and caught."""
        with pytest.raises(BitDubberError) as exc_info:
            raise BitDubberError("Test error")

        assert str(exc_info.value) == "Test error"

    @pytest.mark.unit
    def test_exception_hierarchy(self):
        """Test exception inheritance hierarchy."""
        errors = [
            ScreenCaptureError("test"),
            VoiceRecognitionError("test"),
            ActionExecutionError("test"),
            ConfigurationError("test"),
        ]

        for error in errors:
            assert isinstance(error, BitDubberError)
            assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_catch_base_exception(self):
        """Test catching specific exceptions with base class."""
        with pytest.raises(BitDubberError):
            raise ScreenCaptureError("Test error")

        with pytest.raises(BitDubberError):
            raise VoiceRecognitionError("Test error")

        with pytest.raises(BitDubberError):
            raise ActionExecutionError("Test error")

        with pytest.raises(BitDubberError):
            raise ConfigurationError("Test error")

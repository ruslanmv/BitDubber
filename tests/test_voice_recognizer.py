"""Unit tests for the VoiceRecognizer module."""

from unittest.mock import MagicMock, patch

import pytest
import speech_recognition as sr

from bitdubber.core.voice_recognizer import VoiceRecognizer
from bitdubber.utils.exceptions import VoiceRecognitionError


@pytest.fixture
def voice_recognizer():
    """Provide a VoiceRecognizer instance for testing."""
    return VoiceRecognizer()


@pytest.fixture
def mock_microphone():
    """Provide a mock microphone for testing."""
    mic = MagicMock(spec=sr.Microphone)
    mic.__enter__ = MagicMock(return_value=mic)
    mic.__exit__ = MagicMock(return_value=False)
    return mic


class TestVoiceRecognizer:
    """Test cases for VoiceRecognizer class."""

    @pytest.mark.unit
    def test_initialization(self, voice_recognizer):
        """Test VoiceRecognizer initialization."""
        assert voice_recognizer is not None
        assert voice_recognizer.recognizer is not None
        assert voice_recognizer.microphone is None
        assert voice_recognizer.last_command == ""

    @pytest.mark.unit
    @patch("bitdubber.core.voice_recognizer.sr.Microphone")
    def test_initialize_microphone_success(self, mock_mic_class, voice_recognizer, mock_microphone):
        """Test successful microphone initialization."""
        mock_mic_class.return_value = mock_microphone

        voice_recognizer.initialize_microphone()

        assert voice_recognizer.microphone is not None
        mock_mic_class.assert_called_once()

    @pytest.mark.unit
    @patch("bitdubber.core.voice_recognizer.sr.Microphone")
    def test_initialize_microphone_failure(self, mock_mic_class, voice_recognizer):
        """Test microphone initialization failure handling."""
        mock_mic_class.side_effect = Exception("Microphone not found")

        with pytest.raises(VoiceRecognitionError):
            voice_recognizer.initialize_microphone()

    @pytest.mark.unit
    @patch.object(VoiceRecognizer, "initialize_microphone")
    def test_listen_for_command_success(self, mock_init, voice_recognizer, mock_microphone):
        """Test successful command recognition."""
        voice_recognizer.microphone = mock_microphone

        mock_audio = MagicMock()
        voice_recognizer.recognizer.listen = MagicMock(return_value=mock_audio)
        voice_recognizer.recognizer.recognize_google = MagicMock(
            return_value="open browser"
        )

        result = voice_recognizer.listen_for_command()

        assert result == "open browser"
        assert voice_recognizer.last_command == "open browser"

    @pytest.mark.unit
    @patch.object(VoiceRecognizer, "initialize_microphone")
    def test_listen_for_command_timeout(self, mock_init, voice_recognizer, mock_microphone):
        """Test command recognition timeout."""
        voice_recognizer.microphone = mock_microphone
        voice_recognizer.recognizer.listen = MagicMock(
            side_effect=sr.WaitTimeoutError("Timeout")
        )

        with pytest.raises(VoiceRecognitionError):
            voice_recognizer.listen_for_command()

    @pytest.mark.unit
    @patch.object(VoiceRecognizer, "initialize_microphone")
    def test_listen_for_command_unknown_value(self, mock_init, voice_recognizer, mock_microphone):
        """Test handling of unintelligible audio."""
        voice_recognizer.microphone = mock_microphone

        mock_audio = MagicMock()
        voice_recognizer.recognizer.listen = MagicMock(return_value=mock_audio)
        voice_recognizer.recognizer.recognize_google = MagicMock(
            side_effect=sr.UnknownValueError()
        )

        with pytest.raises(VoiceRecognitionError):
            voice_recognizer.listen_for_command()

    @pytest.mark.unit
    @patch.object(VoiceRecognizer, "initialize_microphone")
    def test_listen_for_command_request_error(self, mock_init, voice_recognizer, mock_microphone):
        """Test handling of API request errors."""
        voice_recognizer.microphone = mock_microphone

        mock_audio = MagicMock()
        voice_recognizer.recognizer.listen = MagicMock(return_value=mock_audio)
        voice_recognizer.recognizer.recognize_google = MagicMock(
            side_effect=sr.RequestError("API error")
        )

        with pytest.raises(VoiceRecognitionError):
            voice_recognizer.listen_for_command()

    @pytest.mark.unit
    @patch("bitdubber.core.voice_recognizer.sr.Microphone.list_microphone_names")
    def test_get_available_microphones(self, mock_list, voice_recognizer):
        """Test getting available microphones."""
        mock_list.return_value = ["Microphone 1", "Microphone 2"]

        mics = voice_recognizer.get_available_microphones()

        assert len(mics) == 2
        assert mics[0] == "Microphone 1"
        assert mics[1] == "Microphone 2"

    @pytest.mark.unit
    def test_parse_command_open(self, voice_recognizer):
        """Test parsing 'open' command."""
        parsed = voice_recognizer.parse_command("open browser")

        assert parsed["action"] == "open"
        assert parsed["target"] == "browser"

    @pytest.mark.unit
    def test_parse_command_click(self, voice_recognizer):
        """Test parsing 'click' command."""
        parsed = voice_recognizer.parse_command("click button")

        assert parsed["action"] == "click"
        assert parsed["target"] == "button"

    @pytest.mark.unit
    def test_parse_command_search(self, voice_recognizer):
        """Test parsing 'search' command."""
        parsed = voice_recognizer.parse_command("search python documentation")

        assert parsed["action"] == "search"
        assert parsed["target"] == "python documentation"

    @pytest.mark.unit
    def test_parse_command_unknown(self, voice_recognizer):
        """Test parsing unknown command."""
        parsed = voice_recognizer.parse_command("hello world")

        assert parsed["action"] == "unknown"
        assert parsed["target"] == "hello world"

    @pytest.mark.unit
    def test_parse_command_case_insensitive(self, voice_recognizer):
        """Test case-insensitive command parsing."""
        parsed = voice_recognizer.parse_command("OPEN Calculator")

        assert parsed["action"] == "open"
        assert parsed["target"] == "calculator"

    @pytest.mark.integration
    @patch.object(VoiceRecognizer, "listen_for_command")
    def test_listen_continuously_stop_phrase(self, mock_listen, voice_recognizer, mock_microphone):
        """Test continuous listening with stop phrase."""
        voice_recognizer.microphone = mock_microphone
        mock_listen.side_effect = ["open browser", "stop listening"]

        callback = MagicMock()
        voice_recognizer.listen_continuously(callback, stop_phrase="stop listening")

        # Callback should be called once (for "open browser")
        callback.assert_called_once_with("open browser")

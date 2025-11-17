"""Tests for Watson services integration.

Author: Ruslan Magana
Website: ruslanmv.com
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from bitdubber.app import BitDubberConfig, WatsonServices, WatsonServicesError


class TestWatsonServices:
    """Test cases for WatsonServices class."""

    @pytest.fixture
    def mock_config(self, monkeypatch: pytest.MonkeyPatch) -> BitDubberConfig:
        """Create mock configuration."""
        env_vars = {
            "TTS_API_KEY": "test_tts_key",
            "TTS_URL": "https://test-tts.url",
            "STT_API_KEY": "test_stt_key",
            "STT_URL": "https://test-stt.url",
            "WATSONX_APIKEY": "test_watsonx_key",
            "PROJECT_ID": "test_project_id",
        }

        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        return BitDubberConfig()

    @patch("bitdubber.app.TextToSpeechV1")
    @patch("bitdubber.app.SpeechToTextV1")
    @patch("bitdubber.app.IAMAuthenticator")
    def test_watson_services_initialization(
        self,
        mock_authenticator: Mock,
        mock_stt: Mock,
        mock_tts: Mock,
        mock_config: BitDubberConfig,
    ) -> None:
        """Test Watson services initialize correctly."""
        watson = WatsonServices(mock_config)

        assert watson.text_to_speech is not None
        assert watson.speech_to_text is not None
        assert mock_authenticator.call_count == 2

    @patch("bitdubber.app.TextToSpeechV1")
    @patch("bitdubber.app.SpeechToTextV1")
    @patch("bitdubber.app.IAMAuthenticator")
    def test_convert_speech_to_text_success(
        self,
        mock_authenticator: Mock,
        mock_stt_class: Mock,
        mock_tts: Mock,
        mock_config: BitDubberConfig,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Test successful speech-to-text conversion."""
        # Create temporary audio file
        audio_file = tmp_path / "test_audio.wav"
        audio_file.write_bytes(b"fake audio data")

        # Mock Watson response
        mock_stt = mock_stt_class.return_value
        mock_response = {
            "results": [{"alternatives": [{"transcript": "Hello world", "confidence": 0.95}]}]
        }
        mock_stt.recognize.return_value.get_result.return_value = mock_response

        watson = WatsonServices(mock_config)
        result = watson.convert_speech_to_text(str(audio_file))

        assert result == "Hello world"
        mock_stt.recognize.assert_called_once()

    @patch("bitdubber.app.TextToSpeechV1")
    @patch("bitdubber.app.SpeechToTextV1")
    @patch("bitdubber.app.IAMAuthenticator")
    def test_convert_speech_to_text_file_not_found(
        self,
        mock_authenticator: Mock,
        mock_stt: Mock,
        mock_tts: Mock,
        mock_config: BitDubberConfig,
    ) -> None:
        """Test speech-to-text with non-existent file."""
        watson = WatsonServices(mock_config)

        with pytest.raises(WatsonServicesError, match="Audio file not found"):
            watson.convert_speech_to_text("nonexistent_file.wav")

    @patch("bitdubber.app.TextToSpeechV1")
    @patch("bitdubber.app.SpeechToTextV1")
    @patch("bitdubber.app.IAMAuthenticator")
    def test_convert_speech_to_text_no_results(
        self,
        mock_authenticator: Mock,
        mock_stt_class: Mock,
        mock_tts: Mock,
        mock_config: BitDubberConfig,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Test speech-to-text with no detected speech."""
        audio_file = tmp_path / "silent_audio.wav"
        audio_file.write_bytes(b"silent audio data")

        mock_stt = mock_stt_class.return_value
        mock_stt.recognize.return_value.get_result.return_value = {"results": []}

        watson = WatsonServices(mock_config)

        with pytest.raises(WatsonServicesError, match="No speech detected"):
            watson.convert_speech_to_text(str(audio_file))

    @patch("bitdubber.app.TextToSpeechV1")
    @patch("bitdubber.app.SpeechToTextV1")
    @patch("bitdubber.app.IAMAuthenticator")
    def test_convert_text_to_speech_success(
        self,
        mock_authenticator: Mock,
        mock_stt: Mock,
        mock_tts_class: Mock,
        mock_config: BitDubberConfig,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Test successful text-to-speech conversion."""
        output_file = tmp_path / "output.wav"

        mock_tts = mock_tts_class.return_value
        mock_response = Mock()
        mock_response.content = b"fake audio content"
        mock_tts.synthesize.return_value.get_result.return_value = mock_response

        watson = WatsonServices(mock_config)
        watson.convert_text_to_speech("Hello world", str(output_file))

        assert output_file.exists()
        assert output_file.read_bytes() == b"fake audio content"
        mock_tts.synthesize.assert_called_once()

    @patch("bitdubber.app.TextToSpeechV1")
    @patch("bitdubber.app.SpeechToTextV1")
    @patch("bitdubber.app.IAMAuthenticator")
    def test_convert_text_to_speech_with_custom_voice(
        self,
        mock_authenticator: Mock,
        mock_stt: Mock,
        mock_tts_class: Mock,
        mock_config: BitDubberConfig,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Test text-to-speech with custom voice model."""
        output_file = tmp_path / "output.wav"

        mock_tts = mock_tts_class.return_value
        mock_response = Mock()
        mock_response.content = b"fake audio content"
        mock_tts.synthesize.return_value.get_result.return_value = mock_response

        watson = WatsonServices(mock_config)
        watson.convert_text_to_speech(
            "Hello world", str(output_file), voice="en-GB_KateVoice"
        )

        # Verify custom voice was used
        call_kwargs = mock_tts.synthesize.call_args[1]
        assert call_kwargs["voice"] == "en-GB_KateVoice"

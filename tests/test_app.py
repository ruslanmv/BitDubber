"""Tests for BitDubber main application module.

Author: Ruslan Magana
Website: ruslanmv.com
"""

import os
from unittest.mock import MagicMock, Mock, patch

import pytest

from bitdubber.app import (
    BitDubberApp,
    BitDubberConfig,
    LLaMAServiceError,
    UIAutomationError,
    WatsonServicesError,
)


class TestBitDubberConfig:
    """Test cases for BitDubberConfig class."""

    def test_config_initialization_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test successful configuration initialization."""
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

        config = BitDubberConfig()

        assert config.tts_api_key == "test_tts_key"
        assert config.stt_api_key == "test_stt_key"
        assert config.watsonx_api_key == "test_watsonx_key"
        assert config.project_id == "test_project_id"

    def test_config_missing_required_variable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration fails when required variable is missing."""
        monkeypatch.delenv("TTS_API_KEY", raising=False)

        with pytest.raises(ValueError, match="Required environment variable"):
            BitDubberConfig()

    def test_config_default_watsonx_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test default WatsonX URL is used when not provided."""
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

        monkeypatch.delenv("WATSONX_URL", raising=False)

        config = BitDubberConfig()
        assert config.watsonx_url == "https://eu-de.ml.cloud.ibm.com"


class TestBitDubberApp:
    """Test cases for BitDubberApp class."""

    @pytest.fixture
    def mock_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Set up mock environment configuration."""
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

    @patch("bitdubber.app.WatsonServices")
    @patch("bitdubber.app.LLaMAService")
    @patch("bitdubber.app.ScreenAutomation")
    def test_app_initialization(
        self,
        mock_automation: Mock,
        mock_llama: Mock,
        mock_watson: Mock,
        mock_config: None,
    ) -> None:
        """Test BitDubber app initializes correctly."""
        app = BitDubberApp()

        assert app.config is not None
        assert app.watson is not None
        assert app.llama is not None
        assert app.automation is not None

    @patch("bitdubber.app.WatsonServices")
    @patch("bitdubber.app.LLaMAService")
    @patch("bitdubber.app.ScreenAutomation")
    def test_handle_user_request_success(
        self,
        mock_automation_class: Mock,
        mock_llama_class: Mock,
        mock_watson_class: Mock,
        mock_config: None,
    ) -> None:
        """Test successful user request handling."""
        # Setup mocks
        mock_watson = mock_watson_class.return_value
        mock_watson.convert_speech_to_text.return_value = "Open Wikipedia"
        mock_watson.convert_text_to_speech.return_value = None

        mock_automation = mock_automation_class.return_value
        mock_automation.take_screenshot.return_value = "screenshot.png"
        mock_automation.execute_click_sequence.return_value = "Execution completed successfully."

        mock_llama = mock_llama_class.return_value
        mock_llama.identify_ui_elements.return_value = "ui_elements.csv"
        mock_llama.determine_click_sequence.return_value = [
            {"action": "click", "coordinates": (100, 100)}
        ]

        app = BitDubberApp()
        result = app.handle_user_request("test_audio.wav")

        assert "Success" in result
        mock_watson.convert_speech_to_text.assert_called_once()
        mock_automation.take_screenshot.assert_called_once()
        mock_llama.identify_ui_elements.assert_called_once()

    @patch("bitdubber.app.WatsonServices")
    @patch("bitdubber.app.LLaMAService")
    @patch("bitdubber.app.ScreenAutomation")
    def test_handle_user_request_watson_error(
        self,
        mock_automation_class: Mock,
        mock_llama_class: Mock,
        mock_watson_class: Mock,
        mock_config: None,
    ) -> None:
        """Test user request handling with Watson error."""
        mock_watson = mock_watson_class.return_value
        mock_watson.convert_speech_to_text.side_effect = WatsonServicesError("Watson error")

        app = BitDubberApp()
        result = app.handle_user_request("test_audio.wav")

        assert "Watson service error" in result

    @patch("bitdubber.app.WatsonServices")
    @patch("bitdubber.app.LLaMAService")
    @patch("bitdubber.app.ScreenAutomation")
    @patch("bitdubber.app.gr.Interface")
    def test_create_interface(
        self,
        mock_interface: Mock,
        mock_automation_class: Mock,
        mock_llama_class: Mock,
        mock_watson_class: Mock,
        mock_config: None,
    ) -> None:
        """Test Gradio interface creation."""
        app = BitDubberApp()
        interface = app.create_interface()

        mock_interface.assert_called_once()
        # Verify interface was created with correct parameters
        call_kwargs = mock_interface.call_args[1]
        assert "title" in call_kwargs
        assert "BitDubber" in call_kwargs["title"]

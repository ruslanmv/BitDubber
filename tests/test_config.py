"""Unit tests for the configuration module."""

from pathlib import Path

import pytest

from bitdubber.config.settings import Settings, get_settings


class TestSettings:
    """Test cases for Settings class."""

    @pytest.mark.unit
    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()

        assert settings.app_name == "BitDubber"
        assert settings.app_version == "0.1.0"
        assert settings.debug is False
        assert settings.log_level == "INFO"

    @pytest.mark.unit
    def test_screenshot_settings(self):
        """Test screenshot-related settings."""
        settings = Settings()

        assert settings.screenshot_dir == Path("screenshots")
        assert settings.screenshot_interval == 1.0
        assert 0.1 <= settings.screenshot_interval <= 60.0

    @pytest.mark.unit
    def test_ocr_settings(self):
        """Test OCR-related settings."""
        settings = Settings()

        assert settings.ocr_language == "eng"
        assert settings.ocr_confidence_threshold == 60.0
        assert 0.0 <= settings.ocr_confidence_threshold <= 100.0

    @pytest.mark.unit
    def test_voice_settings(self):
        """Test voice recognition settings."""
        settings = Settings()

        assert settings.voice_language == "en-US"
        assert settings.voice_timeout == 5.0
        assert settings.voice_phrase_time_limit == 10.0
        assert settings.voice_energy_threshold == 300

    @pytest.mark.unit
    def test_action_settings(self):
        """Test action execution settings."""
        settings = Settings()

        assert settings.action_timeout == 30.0
        assert 1.0 <= settings.action_timeout <= 300.0

    @pytest.mark.unit
    def test_custom_settings(self, tmp_path):
        """Test creating settings with custom values."""
        custom_screenshot_dir = tmp_path / "custom_screenshots"

        settings = Settings(
            app_name="TestApp",
            debug=True,
            log_level="DEBUG",
            screenshot_dir=custom_screenshot_dir,
            ocr_language="spa",
            voice_language="es-ES",
        )

        assert settings.app_name == "TestApp"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.screenshot_dir == custom_screenshot_dir
        assert settings.ocr_language == "spa"
        assert settings.voice_language == "es-ES"

    @pytest.mark.unit
    def test_screenshot_dir_creation(self, tmp_path):
        """Test that screenshot directory is created."""
        screenshot_dir = tmp_path / "screenshots"

        settings = Settings(screenshot_dir=screenshot_dir)

        assert screenshot_dir.exists()
        assert screenshot_dir.is_dir()

    @pytest.mark.unit
    def test_get_settings_caching(self):
        """Test that get_settings returns cached instance."""
        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    @pytest.mark.unit
    def test_settings_validation_screenshot_interval_min(self):
        """Test screenshot interval minimum validation."""
        with pytest.raises(ValueError):
            Settings(screenshot_interval=0.05)  # Below minimum of 0.1

    @pytest.mark.unit
    def test_settings_validation_screenshot_interval_max(self):
        """Test screenshot interval maximum validation."""
        with pytest.raises(ValueError):
            Settings(screenshot_interval=61.0)  # Above maximum of 60.0

    @pytest.mark.unit
    def test_settings_validation_ocr_confidence_min(self):
        """Test OCR confidence minimum validation."""
        with pytest.raises(ValueError):
            Settings(ocr_confidence_threshold=-1.0)  # Below minimum of 0.0

    @pytest.mark.unit
    def test_settings_validation_ocr_confidence_max(self):
        """Test OCR confidence maximum validation."""
        with pytest.raises(ValueError):
            Settings(ocr_confidence_threshold=101.0)  # Above maximum of 100.0

    @pytest.mark.unit
    def test_settings_validation_voice_timeout_min(self):
        """Test voice timeout minimum validation."""
        with pytest.raises(ValueError):
            Settings(voice_timeout=0.5)  # Below minimum of 1.0

    @pytest.mark.unit
    def test_settings_validation_voice_timeout_max(self):
        """Test voice timeout maximum validation."""
        with pytest.raises(ValueError):
            Settings(voice_timeout=31.0)  # Above maximum of 30.0

    @pytest.mark.unit
    def test_settings_validation_energy_threshold_min(self):
        """Test energy threshold minimum validation."""
        with pytest.raises(ValueError):
            Settings(voice_energy_threshold=50)  # Below minimum of 100

    @pytest.mark.unit
    def test_settings_validation_energy_threshold_max(self):
        """Test energy threshold maximum validation."""
        with pytest.raises(ValueError):
            Settings(voice_energy_threshold=4001)  # Above maximum of 4000

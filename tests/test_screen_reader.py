"""Unit tests for the ScreenReader module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from bitdubber.core.screen_reader import ScreenReader
from bitdubber.utils.exceptions import ScreenCaptureError


@pytest.fixture
def screen_reader():
    """Provide a ScreenReader instance for testing."""
    return ScreenReader()


@pytest.fixture
def mock_image():
    """Provide a mock PIL Image for testing."""
    return Image.new("RGB", (100, 100), color="white")


class TestScreenReader:
    """Test cases for ScreenReader class."""

    @pytest.mark.unit
    def test_initialization(self, screen_reader):
        """Test ScreenReader initialization."""
        assert screen_reader is not None
        assert screen_reader.last_screenshot is None
        assert screen_reader.last_text == ""

    @pytest.mark.unit
    @patch("bitdubber.core.screen_reader.ImageGrab.grab")
    def test_capture_screenshot_without_save(self, mock_grab, screen_reader, mock_image):
        """Test capturing screenshot without saving."""
        mock_grab.return_value = mock_image

        result = screen_reader.capture_screenshot(save=False)

        assert isinstance(result, Image.Image)
        assert screen_reader.last_screenshot is None
        mock_grab.assert_called_once()

    @pytest.mark.unit
    @patch("bitdubber.core.screen_reader.ImageGrab.grab")
    def test_capture_screenshot_with_save(self, mock_grab, screen_reader, mock_image, tmp_path):
        """Test capturing screenshot with saving."""
        mock_grab.return_value = mock_image
        screen_reader.settings.screenshot_dir = tmp_path

        result = screen_reader.capture_screenshot(save=True)

        assert isinstance(result, Image.Image)
        assert screen_reader.last_screenshot is not None
        assert screen_reader.last_screenshot.exists()

    @pytest.mark.unit
    @patch("bitdubber.core.screen_reader.ImageGrab.grab")
    def test_capture_screenshot_failure(self, mock_grab, screen_reader):
        """Test screenshot capture failure handling."""
        mock_grab.side_effect = Exception("Capture failed")

        with pytest.raises(ScreenCaptureError):
            screen_reader.capture_screenshot()

    @pytest.mark.unit
    @patch("bitdubber.core.screen_reader.pytesseract.image_to_string")
    def test_extract_text(self, mock_ocr, screen_reader, mock_image):
        """Test text extraction from image."""
        mock_ocr.return_value = "Test text"

        result = screen_reader.extract_text(mock_image, enhance=False)

        assert result == "Test text"
        assert screen_reader.last_text == "Test text"
        mock_ocr.assert_called_once()

    @pytest.mark.unit
    @patch("bitdubber.core.screen_reader.pytesseract.image_to_string")
    def test_extract_text_failure(self, mock_ocr, screen_reader, mock_image):
        """Test text extraction failure handling."""
        mock_ocr.side_effect = Exception("OCR failed")

        with pytest.raises(ScreenCaptureError):
            screen_reader.extract_text(mock_image)

    @pytest.mark.unit
    @patch("bitdubber.core.screen_reader.pytesseract.image_to_data")
    def test_extract_text_with_confidence(self, mock_ocr_data, screen_reader, mock_image):
        """Test text extraction with confidence scores."""
        mock_ocr_data.return_value = {
            "text": ["Test", "text"],
            "conf": [85.0, 90.0],
            "left": [0, 50],
            "top": [0, 0],
            "width": [50, 50],
            "height": [20, 20],
        }

        results = screen_reader.extract_text_with_confidence(mock_image)

        assert len(results) == 2
        assert results[0]["text"] == "Test"
        assert results[0]["confidence"] == 85.0

    @pytest.mark.unit
    @patch.object(ScreenReader, "capture_screenshot")
    @patch.object(ScreenReader, "extract_text")
    def test_capture_and_read(self, mock_extract, mock_capture, screen_reader, mock_image):
        """Test combined capture and read operation."""
        mock_capture.return_value = mock_image
        mock_extract.return_value = "Test text"

        result = screen_reader.capture_and_read()

        assert result == "Test text"
        mock_capture.assert_called_once()
        mock_extract.assert_called_once()

    @pytest.mark.unit
    @patch.object(ScreenReader, "capture_and_read")
    def test_find_text_on_screen_found(self, mock_read, screen_reader):
        """Test finding text on screen when present."""
        mock_read.return_value = "This is a test screen with Settings menu"

        result = screen_reader.find_text_on_screen("Settings")

        assert result is True

    @pytest.mark.unit
    @patch.object(ScreenReader, "capture_and_read")
    def test_find_text_on_screen_not_found(self, mock_read, screen_reader):
        """Test finding text on screen when not present."""
        mock_read.return_value = "This is a test screen"

        result = screen_reader.find_text_on_screen("Settings")

        assert result is False

    @pytest.mark.unit
    @patch.object(ScreenReader, "capture_and_read")
    def test_find_text_case_insensitive(self, mock_read, screen_reader):
        """Test case-insensitive text search."""
        mock_read.return_value = "This is a TEST screen"

        result = screen_reader.find_text_on_screen("test", case_sensitive=False)

        assert result is True

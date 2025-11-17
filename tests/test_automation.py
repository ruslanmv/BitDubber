"""Tests for UI automation and screen capture.

Author: Ruslan Magana
Website: ruslanmv.com
"""

from unittest.mock import Mock, patch

import pytest

from bitdubber.app import ScreenAutomation, UIAutomationError


class TestScreenAutomation:
    """Test cases for ScreenAutomation class."""

    @patch("bitdubber.app.pyautogui.screenshot")
    def test_take_screenshot_success(self, mock_screenshot: Mock, tmp_path: pytest.TempPathFactory) -> None:
        """Test successful screenshot capture."""
        output_path = tmp_path / "test_screenshot.png"

        # Mock screenshot object
        mock_img = Mock()
        mock_screenshot.return_value = mock_img

        result = ScreenAutomation.take_screenshot(str(output_path))

        assert result == str(output_path)
        mock_screenshot.assert_called_once()
        mock_img.save.assert_called_once_with(str(output_path))

    @patch("bitdubber.app.pyautogui.screenshot")
    def test_take_screenshot_failure(self, mock_screenshot: Mock) -> None:
        """Test screenshot capture failure."""
        mock_screenshot.side_effect = Exception("Screenshot failed")

        with pytest.raises(UIAutomationError, match="Failed to take screenshot"):
            ScreenAutomation.take_screenshot()

    def test_encode_image_to_base64_success(self, tmp_path: pytest.TempPathFactory) -> None:
        """Test successful image encoding to base64."""
        # Create test image file
        image_file = tmp_path / "test_image.png"
        test_data = b"fake image data"
        image_file.write_bytes(test_data)

        result = ScreenAutomation.encode_image_to_base64(str(image_file))

        assert isinstance(result, str)
        assert len(result) > 0

        # Verify it's valid base64
        import base64

        decoded = base64.b64decode(result)
        assert decoded == test_data

    def test_encode_image_to_base64_file_not_found(self) -> None:
        """Test image encoding with non-existent file."""
        with pytest.raises(UIAutomationError, match="Image file not found"):
            ScreenAutomation.encode_image_to_base64("nonexistent_image.png")

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_click_action(self, mock_pyautogui: Mock) -> None:
        """Test execution of click action."""
        click_sequence = [{"action": "click", "coordinates": (100, 200)}]

        result = ScreenAutomation.execute_click_sequence(click_sequence)

        assert result == "Execution completed successfully."
        mock_pyautogui.moveTo.assert_called_once_with(100, 200)
        mock_pyautogui.click.assert_called_once()

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_type_action(self, mock_pyautogui: Mock) -> None:
        """Test execution of type action."""
        click_sequence = [{"action": "type", "text": "Hello World"}]

        result = ScreenAutomation.execute_click_sequence(click_sequence)

        assert result == "Execution completed successfully."
        mock_pyautogui.typewrite.assert_called_once_with("Hello World", interval=0.05)

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_press_action(self, mock_pyautogui: Mock) -> None:
        """Test execution of press action."""
        click_sequence = [{"action": "press", "key": "enter"}]

        result = ScreenAutomation.execute_click_sequence(click_sequence)

        assert result == "Execution completed successfully."
        mock_pyautogui.press.assert_called_once_with("enter")

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_multiple_actions(self, mock_pyautogui: Mock) -> None:
        """Test execution of multiple actions in sequence."""
        click_sequence = [
            {"action": "click", "coordinates": (50, 100)},
            {"action": "type", "text": "test"},
            {"action": "press", "key": "tab"},
        ]

        result = ScreenAutomation.execute_click_sequence(click_sequence)

        assert result == "Execution completed successfully."
        assert mock_pyautogui.moveTo.call_count == 1
        assert mock_pyautogui.click.call_count == 1
        assert mock_pyautogui.typewrite.call_count == 1
        assert mock_pyautogui.press.call_count == 1

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_unknown_action(self, mock_pyautogui: Mock) -> None:
        """Test execution with unknown action type."""
        click_sequence = [{"action": "unknown_action", "data": "test"}]

        # Should complete without error but log warning
        result = ScreenAutomation.execute_click_sequence(click_sequence)

        assert result == "Execution completed successfully."

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_failure(self, mock_pyautogui: Mock) -> None:
        """Test execution failure handling."""
        mock_pyautogui.moveTo.side_effect = Exception("Automation failed")
        click_sequence = [{"action": "click", "coordinates": (100, 100)}]

        with pytest.raises(UIAutomationError, match="Failed to execute action sequence"):
            ScreenAutomation.execute_click_sequence(click_sequence)

    @patch("bitdubber.app.pyautogui")
    def test_execute_click_sequence_empty_list(self, mock_pyautogui: Mock) -> None:
        """Test execution with empty action list."""
        result = ScreenAutomation.execute_click_sequence([])

        assert result == "Execution completed successfully."
        mock_pyautogui.moveTo.assert_not_called()
        mock_pyautogui.click.assert_not_called()

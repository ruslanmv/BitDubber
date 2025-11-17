"""Screen reading and analysis module.

This module provides functionality to capture and analyze screen content
using OCR and image processing techniques.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageGrab

from bitdubber.config import get_settings
from bitdubber.utils.exceptions import ScreenCaptureError
from bitdubber.utils.logger import get_logger

logger = get_logger(__name__)


class ScreenReader:
    """Screen reading and analysis class.

    This class handles capturing screenshots, performing OCR,
    and analyzing screen content.

    Attributes:
        settings: Application settings instance.
        last_screenshot: Path to the last captured screenshot.
        last_text: Last extracted text from screen.

    Example:
        >>> reader = ScreenReader()
        >>> text = reader.capture_and_read()
        >>> print(f"Screen text: {text}")
    """

    def __init__(self) -> None:
        """Initialize the ScreenReader."""
        self.settings = get_settings()
        self.last_screenshot: Optional[Path] = None
        self.last_text: str = ""
        logger.info("ScreenReader initialized")

    def capture_screenshot(
        self, save: bool = True, bbox: Optional[Tuple[int, int, int, int]] = None
    ) -> Image.Image:
        """Capture a screenshot of the screen.

        Args:
            save: Whether to save the screenshot to disk.
            bbox: Optional bounding box (left, top, right, bottom) to capture
                  a specific region. If None, captures the entire screen.

        Returns:
            PIL Image object of the screenshot.

        Raises:
            ScreenCaptureError: If screenshot capture fails.

        Example:
            >>> reader = ScreenReader()
            >>> img = reader.capture_screenshot()
        """
        try:
            logger.debug(f"Capturing screenshot (save={save}, bbox={bbox})")
            screenshot = ImageGrab.grab(bbox=bbox)

            if save:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = self.settings.screenshot_dir / filename
                screenshot.save(filepath)
                self.last_screenshot = filepath
                logger.info(f"Screenshot saved to {filepath}")

            return screenshot

        except Exception as e:
            error_msg = "Failed to capture screenshot"
            logger.error(f"{error_msg}: {str(e)}")
            raise ScreenCaptureError(error_msg, details=str(e)) from e

    def extract_text(
        self, image: Optional[Image.Image] = None, enhance: bool = True
    ) -> str:
        """Extract text from an image using OCR.

        Args:
            image: PIL Image to extract text from. If None, captures a new screenshot.
            enhance: Whether to enhance the image before OCR.

        Returns:
            Extracted text from the image.

        Raises:
            ScreenCaptureError: If text extraction fails.

        Example:
            >>> reader = ScreenReader()
            >>> text = reader.extract_text()
        """
        try:
            if image is None:
                image = self.capture_screenshot(save=False)

            if enhance:
                image = self._enhance_image(image)

            # Perform OCR
            custom_config = f"--oem 3 --psm 6 -l {self.settings.ocr_language}"
            text = pytesseract.image_to_string(image, config=custom_config)

            self.last_text = text.strip()
            logger.debug(f"Extracted text length: {len(self.last_text)} characters")

            return self.last_text

        except Exception as e:
            error_msg = "Failed to extract text from image"
            logger.error(f"{error_msg}: {str(e)}")
            raise ScreenCaptureError(error_msg, details=str(e)) from e

    def extract_text_with_confidence(
        self, image: Optional[Image.Image] = None
    ) -> List[Dict[str, any]]:
        """Extract text with confidence scores using OCR.

        Args:
            image: PIL Image to extract text from. If None, captures a new screenshot.

        Returns:
            List of dictionaries containing text and confidence scores.

        Raises:
            ScreenCaptureError: If text extraction fails.

        Example:
            >>> reader = ScreenReader()
            >>> results = reader.extract_text_with_confidence()
            >>> for item in results:
            ...     print(f"{item['text']}: {item['confidence']}%")
        """
        try:
            if image is None:
                image = self.capture_screenshot(save=False)

            # Get detailed OCR data
            data = pytesseract.image_to_data(
                image, output_type=pytesseract.Output.DICT
            )

            results = []
            for i, text in enumerate(data["text"]):
                if text.strip():
                    confidence = float(data["conf"][i])
                    if confidence >= self.settings.ocr_confidence_threshold:
                        results.append(
                            {
                                "text": text,
                                "confidence": confidence,
                                "left": data["left"][i],
                                "top": data["top"][i],
                                "width": data["width"][i],
                                "height": data["height"][i],
                            }
                        )

            logger.debug(
                f"Extracted {len(results)} text elements above confidence threshold"
            )
            return results

        except Exception as e:
            error_msg = "Failed to extract text with confidence"
            logger.error(f"{error_msg}: {str(e)}")
            raise ScreenCaptureError(error_msg, details=str(e)) from e

    def capture_and_read(
        self, save_screenshot: bool = False
    ) -> str:
        """Capture screenshot and extract text in one operation.

        Args:
            save_screenshot: Whether to save the screenshot to disk.

        Returns:
            Extracted text from the screen.

        Example:
            >>> reader = ScreenReader()
            >>> text = reader.capture_and_read()
        """
        screenshot = self.capture_screenshot(save=save_screenshot)
        return self.extract_text(screenshot)

    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image for better OCR results.

        Args:
            image: PIL Image to enhance.

        Returns:
            Enhanced PIL Image.
        """
        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # Apply adaptive thresholding
        enhanced = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Convert back to PIL Image
        return Image.fromarray(enhanced)

    def find_text_on_screen(
        self, search_text: str, case_sensitive: bool = False
    ) -> bool:
        """Search for specific text on the screen.

        Args:
            search_text: Text to search for.
            case_sensitive: Whether the search should be case-sensitive.

        Returns:
            True if text is found on screen, False otherwise.

        Example:
            >>> reader = ScreenReader()
            >>> if reader.find_text_on_screen("Settings"):
            ...     print("Settings menu is visible")
        """
        screen_text = self.capture_and_read()

        if not case_sensitive:
            screen_text = screen_text.lower()
            search_text = search_text.lower()

        found = search_text in screen_text
        logger.debug(f"Text search for '{search_text}': {'Found' if found else 'Not found'}")

        return found

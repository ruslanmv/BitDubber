"""BitDubber Main Application Module.

This module provides the core functionality for the BitDubber desktop assistant,
including speech-to-text, text-to-speech, UI element detection, and automated
action execution using IBM Watson and LLaMA models.

Author: Ruslan Magana
Website: ruslanmv.com
"""

import base64
import logging
import os
import sys
from typing import Any

import gradio as gr
import pandas as pd
import pyautogui
import requests
from dotenv import load_dotenv
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1, TextToSpeechV1

# Load environment variables
load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class WatsonServicesError(Exception):
    """Custom exception for Watson services errors."""

    pass


class LLaMAServiceError(Exception):
    """Custom exception for LLaMA service errors."""

    pass


class UIAutomationError(Exception):
    """Custom exception for UI automation errors."""

    pass


class BitDubberConfig:
    """Configuration manager for BitDubber application.

    This class handles loading and validation of all required environment
    variables and configuration settings.

    Attributes:
        tts_api_key: IBM Watson Text-to-Speech API key
        tts_url: IBM Watson Text-to-Speech service URL
        stt_api_key: IBM Watson Speech-to-Text API key
        stt_url: IBM Watson Speech-to-Text service URL
        watsonx_api_key: IBM WatsonX API key for LLaMA models
        watsonx_url: IBM WatsonX base URL
        project_id: IBM Cloud project ID
    """

    def __init__(self) -> None:
        """Initialize configuration from environment variables."""
        self.tts_api_key = self._get_env_variable("TTS_API_KEY")
        self.tts_url = self._get_env_variable("TTS_URL")
        self.stt_api_key = self._get_env_variable("STT_API_KEY")
        self.stt_url = self._get_env_variable("STT_URL")
        self.watsonx_api_key = self._get_env_variable("WATSONX_APIKEY")
        self.watsonx_url = self._get_env_variable(
            "WATSONX_URL", default="https://eu-de.ml.cloud.ibm.com"
        )
        self.project_id = self._get_env_variable("PROJECT_ID")

        logger.info("Configuration loaded successfully")

    @staticmethod
    def _get_env_variable(key: str, default: str | None = None) -> str:
        """Retrieve environment variable with validation.

        Args:
            key: Environment variable name
            default: Default value if variable is not set

        Returns:
            Value of the environment variable

        Raises:
            ValueError: If required variable is not set and no default provided
        """
        value = os.getenv(key, default)
        if value is None:
            error_msg = f"Required environment variable '{key}' is not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return value


class WatsonServices:
    """Wrapper for IBM Watson Speech services.

    This class provides methods for speech-to-text and text-to-speech
    conversion using IBM Watson APIs.

    Attributes:
        text_to_speech: IBM Watson TextToSpeechV1 instance
        speech_to_text: IBM Watson SpeechToTextV1 instance
    """

    def __init__(self, config: BitDubberConfig) -> None:
        """Initialize Watson services with authentication.

        Args:
            config: BitDubberConfig instance with credentials
        """
        try:
            # Initialize Text-to-Speech
            tts_authenticator = IAMAuthenticator(config.tts_api_key)
            self.text_to_speech = TextToSpeechV1(authenticator=tts_authenticator)
            self.text_to_speech.set_service_url(config.tts_url)

            # Initialize Speech-to-Text
            stt_authenticator = IAMAuthenticator(config.stt_api_key)
            self.speech_to_text = SpeechToTextV1(authenticator=stt_authenticator)
            self.speech_to_text.set_service_url(config.stt_url)

            logger.info("Watson services initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize Watson services: {e}"
            logger.error(error_msg)
            raise WatsonServicesError(error_msg) from e

    def convert_speech_to_text(self, audio_file_path: str) -> str:
        """Convert speech audio file to text.

        Args:
            audio_file_path: Path to the audio file (WAV format)

        Returns:
            Transcribed text from the audio

        Raises:
            WatsonServicesError: If speech recognition fails
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = self.speech_to_text.recognize(
                    audio=audio_file,
                    content_type="audio/wav",
                    timestamps=True,
                    word_confidence=True,
                ).get_result()

            if not response.get("results"):
                raise WatsonServicesError("No speech detected in audio file")

            text = response["results"][0]["alternatives"][0]["transcript"]
            logger.info(f"Speech converted to text: '{text}'")
            return text

        except FileNotFoundError as e:
            error_msg = f"Audio file not found: {audio_file_path}"
            logger.error(error_msg)
            raise WatsonServicesError(error_msg) from e
        except Exception as e:
            error_msg = f"Speech-to-text conversion failed: {e}"
            logger.error(error_msg)
            raise WatsonServicesError(error_msg) from e

    def convert_text_to_speech(
        self, text: str, output_file: str = "output.wav", voice: str = "en-US_AllisonVoice"
    ) -> None:
        """Convert text to speech audio file.

        Args:
            text: Text to convert to speech
            output_file: Path for output audio file
            voice: Voice model to use for synthesis

        Raises:
            WatsonServicesError: If text-to-speech conversion fails
        """
        try:
            response = self.text_to_speech.synthesize(
                text=text, voice=voice, accept="audio/wav"
            ).get_result()

            with open(output_file, "wb") as audio_file:
                audio_file.write(response.content)

            logger.info(f"Text converted to speech and saved to {output_file}")

        except Exception as e:
            error_msg = f"Text-to-speech conversion failed: {e}"
            logger.error(error_msg)
            raise WatsonServicesError(error_msg) from e


class ScreenAutomation:
    """Handles screen capture and UI automation.

    This class provides methods for taking screenshots and executing
    automated UI actions using pyautogui.
    """

    @staticmethod
    def take_screenshot(output_path: str = "screenshot.png") -> str:
        """Capture a screenshot of the current screen.

        Args:
            output_path: Path where screenshot will be saved

        Returns:
            Path to the saved screenshot

        Raises:
            UIAutomationError: If screenshot capture fails
        """
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(output_path)
            logger.info(f"Screenshot saved to {output_path}")
            return output_path

        except Exception as e:
            error_msg = f"Failed to take screenshot: {e}"
            logger.error(error_msg)
            raise UIAutomationError(error_msg) from e

    @staticmethod
    def encode_image_to_base64(file_path: str) -> str:
        """Encode an image file to base64 string.

        Args:
            file_path: Path to the image file

        Returns:
            Base64 encoded string of the image

        Raises:
            UIAutomationError: If image encoding fails
        """
        try:
            with open(file_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("utf-8")
            logger.debug(f"Image {file_path} encoded to base64")
            return encoded

        except FileNotFoundError as e:
            error_msg = f"Image file not found: {file_path}"
            logger.error(error_msg)
            raise UIAutomationError(error_msg) from e
        except Exception as e:
            error_msg = f"Failed to encode image: {e}"
            logger.error(error_msg)
            raise UIAutomationError(error_msg) from e

    @staticmethod
    def execute_click_sequence(click_sequence: list[dict[str, Any]]) -> str:
        """Execute a sequence of UI automation actions.

        Args:
            click_sequence: List of action dictionaries containing action details

        Returns:
            Success message upon completion

        Raises:
            UIAutomationError: If action execution fails
        """
        try:
            for idx, action in enumerate(click_sequence):
                action_type = action.get("action")
                logger.info(f"Executing action {idx + 1}/{len(click_sequence)}: {action_type}")

                if action_type == "click":
                    coordinates = action.get("coordinates")
                    if coordinates:
                        pyautogui.moveTo(*coordinates)
                        pyautogui.click()
                elif action_type == "type":
                    text = action.get("text")
                    if text:
                        pyautogui.typewrite(text, interval=0.05)
                elif action_type == "press":
                    key = action.get("key")
                    if key:
                        pyautogui.press(key)
                else:
                    logger.warning(f"Unknown action type: {action_type}")

            logger.info("Action sequence execution completed successfully")
            return "Execution completed successfully."

        except Exception as e:
            error_msg = f"Failed to execute action sequence: {e}"
            logger.error(error_msg)
            raise UIAutomationError(error_msg) from e


class LLaMAService:
    """Service for interacting with IBM WatsonX LLaMA models.

    This class provides methods for UI element detection and action
    sequence determination using LLaMA 3.2 and LLaMA 3.1 models.

    Attributes:
        config: BitDubberConfig instance
        access_token: IBM Cloud access token (cached)
    """

    def __init__(self, config: BitDubberConfig) -> None:
        """Initialize LLaMA service.

        Args:
            config: BitDubberConfig instance with credentials
        """
        self.config = config
        self.access_token: str | None = None
        logger.info("LLaMA service initialized")

    def get_auth_token(self) -> str:
        """Retrieve IBM Cloud access token.

        Returns:
            Valid IBM Cloud access token

        Raises:
            LLaMAServiceError: If token retrieval fails
        """
        try:
            url = "https://iam.cloud.ibm.com/identity/token"
            data = {
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.config.watsonx_api_key,
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            response = requests.post(url, data=data, headers=headers, timeout=30)
            response.raise_for_status()

            self.access_token = response.json()["access_token"]
            logger.debug("IBM Cloud access token obtained")
            return self.access_token

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to get IBM Cloud access token: {e}"
            logger.error(error_msg)
            raise LLaMAServiceError(error_msg) from e

    def identify_ui_elements(self, screenshot_path: str) -> str:
        """Identify UI elements in screenshot using LLaMA 3.2 Vision model.

        Args:
            screenshot_path: Path to screenshot image

        Returns:
            Path to CSV file containing identified UI elements

        Raises:
            LLaMAServiceError: If UI element identification fails
        """
        try:
            access_token = self.get_auth_token()
            encoded_image = ScreenAutomation.encode_image_to_base64(screenshot_path)

            url = f"{self.config.watsonx_url}/ml/v1/text/chat?version=2023-05-29"
            body = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Extract UI elements from the image with coordinates.",
                    },
                    {"role": "user", "content": encoded_image},
                ],
                "project_id": self.config.project_id,
                "model_id": "meta-llama/llama-3-2-90b-vision-instruct",
            }
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, json=body, headers=headers, timeout=60)
            response.raise_for_status()

            # TODO: Parse actual response from LLaMA model
            # For now, using simulated output
            elements = [
                {"coordinates": (50, 100), "description": "URL Bar"},
                {"coordinates": (200, 300), "description": "Search Button"},
            ]

            df = pd.DataFrame(elements)
            csv_path = "ui_elements.csv"
            df.to_csv(csv_path, index=False)

            logger.info(f"UI elements identified and saved to {csv_path}")
            return csv_path

        except Exception as e:
            error_msg = f"Failed to identify UI elements: {e}"
            logger.error(error_msg)
            raise LLaMAServiceError(error_msg) from e

    def determine_click_sequence(self, user_request: str, csv_path: str) -> list[dict[str, Any]]:
        """Determine action sequence based on user request and UI elements.

        Args:
            user_request: User's voice command text
            csv_path: Path to CSV file with UI elements

        Returns:
            List of action dictionaries

        Raises:
            LLaMAServiceError: If action determination fails
        """
        try:
            df = pd.read_csv(csv_path)
            access_token = self.get_auth_token()

            prompt = (
                f"Given the UI elements: {df.to_dict(orient='records')}, "
                f"which actions should be performed to execute: '{user_request}'? "
                f"Respond in JSON format with actions."
            )

            url = f"{self.config.watsonx_url}/ml/v1/text/chat?version=2023-05-29"
            body = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Provide JSON response with UI actions based on elements.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "project_id": self.config.project_id,
                "model_id": "meta-llama/llama-3-1-90b-instruct",
            }
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, json=body, headers=headers, timeout=60)
            response.raise_for_status()

            # TODO: Parse actual response from LLaMA model
            # For now, using simulated output
            actions = [
                {"action": "click", "coordinates": (50, 100)},
                {"action": "type", "text": "https://www.wikipedia.org"},
                {"action": "press", "key": "enter"},
            ]

            logger.info(f"Click sequence determined with {len(actions)} actions")
            return actions

        except Exception as e:
            error_msg = f"Failed to determine click sequence: {e}"
            logger.error(error_msg)
            raise LLaMAServiceError(error_msg) from e


class BitDubberApp:
    """Main BitDubber application orchestrator.

    This class coordinates all components to handle user voice requests,
    process UI interactions, and execute automated actions.

    Attributes:
        config: Application configuration
        watson: Watson services instance
        llama: LLaMA service instance
        automation: Screen automation instance
    """

    def __init__(self) -> None:
        """Initialize BitDubber application with all services."""
        try:
            self.config = BitDubberConfig()
            self.watson = WatsonServices(self.config)
            self.llama = LLaMAService(self.config)
            self.automation = ScreenAutomation()
            logger.info("BitDubber application initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize BitDubber: {e}")
            raise

    def handle_user_request(self, audio_input: str) -> str:
        """Process user voice request and execute corresponding actions.

        Args:
            audio_input: Path to audio file with user command

        Returns:
            Result message describing execution status
        """
        try:
            # Step 1: Convert speech to text
            logger.info("Processing user voice request")
            user_request = self.watson.convert_speech_to_text(audio_input)

            # Step 2: Take screenshot
            screenshot_path = self.automation.take_screenshot()

            # Step 3: Identify UI elements
            csv_path = self.llama.identify_ui_elements(screenshot_path)

            # Step 4: Determine click sequence
            click_sequence = self.llama.determine_click_sequence(user_request, csv_path)

            # Step 5: Convert planned actions to speech for confirmation
            actions_text = "Planned sequence of actions: " + ", ".join(
                [f"{action.get('action', 'unknown')}" for action in click_sequence]
            )
            self.watson.convert_text_to_speech(actions_text)

            # Step 6: User confirmation (in production, implement proper confirmation UI)
            # For now, auto-confirm in Gradio interface
            logger.info("Auto-confirming action execution in Gradio interface")

            # Step 7: Execute actions
            result = self.automation.execute_click_sequence(click_sequence)

            logger.info("Request handled successfully")
            return f"Success: {result}"

        except WatsonServicesError as e:
            error_msg = f"Watson service error: {e}"
            logger.error(error_msg)
            return error_msg
        except LLaMAServiceError as e:
            error_msg = f"LLaMA service error: {e}"
            logger.error(error_msg)
            return error_msg
        except UIAutomationError as e:
            error_msg = f"UI automation error: {e}"
            logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            return error_msg

    def create_interface(self) -> gr.Interface:
        """Create Gradio web interface for BitDubber.

        Returns:
            Configured Gradio Interface instance
        """
        interface = gr.Interface(
            fn=self.handle_user_request,
            inputs=gr.Audio(sources=["microphone"], type="filepath", label="Voice Command"),
            outputs=gr.Textbox(label="Execution Result"),
            title="🤖 BitDubber - AI Desktop Assistant",
            description=(
                "Speak a command, and BitDubber will identify UI elements "
                "and perform actions accordingly using IBM Watson and LLaMA models."
            ),
            article=(
                "**Author:** Ruslan Magana | **Website:** [ruslanmv.com](https://ruslanmv.com) "
                "| **License:** Apache 2.0"
            ),
            theme=gr.themes.Soft(),
        )

        logger.info("Gradio interface created")
        return interface

    def launch(self, **kwargs: Any) -> None:
        """Launch the Gradio web interface.

        Args:
            **kwargs: Additional arguments passed to Gradio launch()
        """
        try:
            interface = self.create_interface()
            logger.info("Launching BitDubber web interface...")
            interface.launch(**kwargs)

        except Exception as e:
            logger.error(f"Failed to launch interface: {e}")
            raise


def main() -> None:
    """Main entry point for BitDubber application."""
    try:
        logger.info("Starting BitDubber application")
        app = BitDubberApp()
        app.launch()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

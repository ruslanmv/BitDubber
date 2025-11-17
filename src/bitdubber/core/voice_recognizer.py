"""Voice recognition and command processing module.

This module provides functionality to capture and recognize voice commands
using speech recognition.
"""

from typing import Dict, List, Optional

import speech_recognition as sr

from bitdubber.config import get_settings
from bitdubber.utils.exceptions import VoiceRecognitionError
from bitdubber.utils.logger import get_logger

logger = get_logger(__name__)


class VoiceRecognizer:
    """Voice recognition and command processing class.

    This class handles capturing audio input, recognizing speech,
    and processing voice commands.

    Attributes:
        settings: Application settings instance.
        recognizer: Speech recognition instance.
        microphone: Microphone instance for audio input.
        last_command: Last recognized voice command.

    Example:
        >>> recognizer = VoiceRecognizer()
        >>> command = recognizer.listen_for_command()
        >>> print(f"Command: {command}")
    """

    def __init__(self) -> None:
        """Initialize the VoiceRecognizer."""
        self.settings = get_settings()
        self.recognizer = sr.Recognizer()
        self.microphone: Optional[sr.Microphone] = None
        self.last_command: str = ""

        # Configure recognizer
        self.recognizer.energy_threshold = self.settings.voice_energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        logger.info("VoiceRecognizer initialized")

    def initialize_microphone(self, device_index: Optional[int] = None) -> None:
        """Initialize the microphone.

        Args:
            device_index: Optional microphone device index. If None, uses default.

        Raises:
            VoiceRecognitionError: If microphone initialization fails.

        Example:
            >>> recognizer = VoiceRecognizer()
            >>> recognizer.initialize_microphone()
        """
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone initialized successfully")

        except Exception as e:
            error_msg = "Failed to initialize microphone"
            logger.error(f"{error_msg}: {str(e)}")
            raise VoiceRecognitionError(error_msg, details=str(e)) from e

    def listen_for_command(
        self, timeout: Optional[float] = None, phrase_time_limit: Optional[float] = None
    ) -> str:
        """Listen for a voice command.

        Args:
            timeout: Maximum time to wait for speech to start (seconds).
                    If None, uses settings default.
            phrase_time_limit: Maximum time for the phrase (seconds).
                              If None, uses settings default.

        Returns:
            Recognized voice command text.

        Raises:
            VoiceRecognitionError: If voice recognition fails.

        Example:
            >>> recognizer = VoiceRecognizer()
            >>> recognizer.initialize_microphone()
            >>> command = recognizer.listen_for_command()
        """
        if self.microphone is None:
            self.initialize_microphone()

        timeout = timeout or self.settings.voice_timeout
        phrase_time_limit = phrase_time_limit or self.settings.voice_phrase_time_limit

        try:
            logger.info("Listening for command...")

            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )

            logger.debug("Processing audio...")
            command = self.recognizer.recognize_google(
                audio, language=self.settings.voice_language
            )

            self.last_command = command
            logger.info(f"Recognized command: {command}")

            return command

        except sr.WaitTimeoutError:
            error_msg = "Listening timed out - no speech detected"
            logger.warning(error_msg)
            raise VoiceRecognitionError(error_msg)

        except sr.UnknownValueError:
            error_msg = "Could not understand audio"
            logger.warning(error_msg)
            raise VoiceRecognitionError(error_msg)

        except sr.RequestError as e:
            error_msg = "Could not request results from speech recognition service"
            logger.error(f"{error_msg}: {str(e)}")
            raise VoiceRecognitionError(error_msg, details=str(e)) from e

        except Exception as e:
            error_msg = "Unexpected error during voice recognition"
            logger.error(f"{error_msg}: {str(e)}")
            raise VoiceRecognitionError(error_msg, details=str(e)) from e

    def listen_continuously(
        self, callback: callable, stop_phrase: str = "stop listening"
    ) -> None:
        """Listen continuously for commands and invoke callback.

        Args:
            callback: Function to call with recognized commands.
                     Should accept a single string parameter.
            stop_phrase: Phrase to stop continuous listening.

        Example:
            >>> def handle_command(cmd: str):
            ...     print(f"Got command: {cmd}")
            >>> recognizer = VoiceRecognizer()
            >>> recognizer.initialize_microphone()
            >>> recognizer.listen_continuously(handle_command)
        """
        if self.microphone is None:
            self.initialize_microphone()

        logger.info(
            f"Starting continuous listening (say '{stop_phrase}' to stop)..."
        )

        while True:
            try:
                command = self.listen_for_command()

                if command.lower() == stop_phrase.lower():
                    logger.info("Stop phrase detected - ending continuous listening")
                    break

                callback(command)

            except VoiceRecognitionError as e:
                logger.debug(f"Recognition error: {e}")
                continue

            except KeyboardInterrupt:
                logger.info("Continuous listening interrupted by user")
                break

    def get_available_microphones(self) -> Dict[int, str]:
        """Get list of available microphone devices.

        Returns:
            Dictionary mapping device index to device name.

        Example:
            >>> recognizer = VoiceRecognizer()
            >>> mics = recognizer.get_available_microphones()
            >>> for idx, name in mics.items():
            ...     print(f"{idx}: {name}")
        """
        microphones = {}
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            microphones[index] = name
            logger.debug(f"Found microphone {index}: {name}")

        return microphones

    def parse_command(
        self, command: Optional[str] = None
    ) -> Dict[str, any]:
        """Parse a voice command into action and parameters.

        Args:
            command: Command to parse. If None, uses last_command.

        Returns:
            Dictionary containing parsed action and parameters.

        Example:
            >>> recognizer = VoiceRecognizer()
            >>> parsed = recognizer.parse_command("open settings menu")
            >>> print(parsed)
            {'action': 'open', 'target': 'settings menu'}
        """
        command = command or self.last_command
        command = command.lower().strip()

        # Basic command parsing - can be extended with NLP
        action_verbs = ["open", "close", "click", "type", "scroll", "search", "find"]

        parsed = {"raw": command, "action": None, "target": None, "params": {}}

        for verb in action_verbs:
            if command.startswith(verb):
                parsed["action"] = verb
                parsed["target"] = command[len(verb) :].strip()
                break

        if parsed["action"] is None:
            # No recognized action verb
            parsed["action"] = "unknown"
            parsed["target"] = command

        logger.debug(f"Parsed command: {parsed}")
        return parsed

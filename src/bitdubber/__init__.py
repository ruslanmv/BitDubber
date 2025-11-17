"""BitDubber - A cutting-edge desktop assistant.

BitDubber combines screen-reading capabilities with intelligent voice commands
to revolutionize how you interact with your computer.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache-2.0
"""

__version__ = "0.1.0"
__author__ = "Ruslan Magana"
__email__ = "contact@ruslanmv.com"
__license__ = "Apache-2.0"

from bitdubber.core.action_executor import ActionExecutor
from bitdubber.core.screen_reader import ScreenReader
from bitdubber.core.voice_recognizer import VoiceRecognizer

__all__ = [
    "ScreenReader",
    "VoiceRecognizer",
    "ActionExecutor",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

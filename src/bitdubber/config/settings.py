"""Application settings and configuration.

This module defines the application settings using Pydantic for validation
and environment variable management.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation.

    This class defines all configuration parameters for BitDubber.
    Settings can be loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="BITDUBBER_",
    )

    # Application settings
    app_name: str = Field(default="BitDubber", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Logging settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_file: Optional[Path] = Field(
        default=None, description="Path to log file (optional)"
    )

    # Screen capture settings
    screenshot_dir: Path = Field(
        default=Path("screenshots"), description="Directory for saving screenshots"
    )
    screenshot_interval: float = Field(
        default=1.0,
        description="Interval between screen captures in seconds",
        ge=0.1,
        le=60.0,
    )

    # OCR settings
    ocr_language: str = Field(default="eng", description="OCR language (e.g., eng)")
    ocr_confidence_threshold: float = Field(
        default=60.0,
        description="Minimum confidence threshold for OCR",
        ge=0.0,
        le=100.0,
    )

    # Voice recognition settings
    voice_language: str = Field(
        default="en-US", description="Voice recognition language"
    )
    voice_timeout: float = Field(
        default=5.0,
        description="Voice recognition timeout in seconds",
        ge=1.0,
        le=30.0,
    )
    voice_phrase_time_limit: float = Field(
        default=10.0,
        description="Maximum phrase time limit in seconds",
        ge=1.0,
        le=60.0,
    )
    voice_energy_threshold: int = Field(
        default=300,
        description="Energy threshold for voice detection",
        ge=100,
        le=4000,
    )

    # Action execution settings
    action_timeout: float = Field(
        default=30.0,
        description="Timeout for action execution in seconds",
        ge=1.0,
        le=300.0,
    )

    def __init__(self, **kwargs):
        """Initialize settings and create necessary directories.

        Args:
            **kwargs: Configuration parameters.
        """
        super().__init__(**kwargs)
        # Create screenshot directory if it doesn't exist
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    This function returns a cached instance of Settings to avoid
    re-reading configuration on every access.

    Returns:
        Settings: The application settings instance.

    Example:
        >>> settings = get_settings()
        >>> print(settings.app_name)
        BitDubber
    """
    return Settings()

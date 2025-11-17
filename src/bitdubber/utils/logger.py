"""Logging configuration for BitDubber.

This module provides centralized logging configuration using loguru.
"""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    log_rotation: str = "10 MB",
    log_retention: str = "1 week",
    log_format: Optional[str] = None,
) -> None:
    """Configure logging for the application.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to log file. If None, logs only to console.
        log_rotation: When to rotate log files (e.g., "10 MB", "1 day").
        log_retention: How long to keep rotated logs (e.g., "1 week", "30 days").
        log_format: Custom log format string. If None, uses default format.

    Example:
        >>> setup_logging(log_level="DEBUG", log_file=Path("app.log"))
    """
    # Remove default handler
    logger.remove()

    # Default format if not provided
    if log_format is None:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    # Add console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True,
    )

    # Add file handler if log file is specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_file),
            format=log_format,
            level=log_level,
            rotation=log_rotation,
            retention=log_retention,
            compression="zip",
        )

    logger.info(f"Logging initialized at level {log_level}")
    if log_file:
        logger.info(f"Log file: {log_file}")


def get_logger(name: str) -> "logger":
    """Get a logger instance with the specified name.

    Args:
        name: The name for the logger (typically __name__).

    Returns:
        A configured logger instance.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return logger.bind(name=name)

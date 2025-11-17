"""Action execution module.

This module provides functionality to execute actions based on
voice commands and screen context.
"""

import subprocess
import time
from typing import Any, Dict, Optional

from bitdubber.config import get_settings
from bitdubber.utils.exceptions import ActionExecutionError
from bitdubber.utils.logger import get_logger

logger = get_logger(__name__)


class ActionExecutor:
    """Action execution class.

    This class handles executing actions based on parsed voice commands
    and screen context.

    Attributes:
        settings: Application settings instance.
        action_history: List of executed actions.

    Example:
        >>> executor = ActionExecutor()
        >>> result = executor.execute_action("open", "browser")
    """

    def __init__(self) -> None:
        """Initialize the ActionExecutor."""
        self.settings = get_settings()
        self.action_history: list = []
        logger.info("ActionExecutor initialized")

    def execute_action(
        self,
        action: str,
        target: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute an action.

        Args:
            action: The action to execute (e.g., 'open', 'close', 'click').
            target: The target of the action (e.g., 'browser', 'file').
            params: Optional additional parameters for the action.

        Returns:
            Dictionary containing execution result and metadata.

        Raises:
            ActionExecutionError: If action execution fails.

        Example:
            >>> executor = ActionExecutor()
            >>> result = executor.execute_action("open", "calculator")
        """
        if params is None:
            params = {}

        logger.info(f"Executing action: {action} on target: {target}")

        try:
            result = self._dispatch_action(action, target, params)

            # Record in history
            self.action_history.append(
                {
                    "action": action,
                    "target": target,
                    "params": params,
                    "result": result,
                    "timestamp": time.time(),
                }
            )

            logger.info(f"Action executed successfully: {action}")
            return result

        except Exception as e:
            error_msg = f"Failed to execute action: {action}"
            logger.error(f"{error_msg}: {str(e)}")
            raise ActionExecutionError(error_msg, details=str(e)) from e

    def _dispatch_action(
        self, action: str, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dispatch action to appropriate handler.

        Args:
            action: The action to execute.
            target: The target of the action.
            params: Additional parameters.

        Returns:
            Dictionary containing execution result.
        """
        action = action.lower()

        action_map = {
            "open": self._action_open,
            "close": self._action_close,
            "click": self._action_click,
            "type": self._action_type,
            "scroll": self._action_scroll,
            "search": self._action_search,
            "find": self._action_find,
        }

        handler = action_map.get(action, self._action_unknown)
        return handler(target, params)

    def _action_open(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'open' action.

        Args:
            target: What to open.
            params: Additional parameters.

        Returns:
            Execution result.
        """
        logger.debug(f"Opening: {target}")

        # Map common application names to commands
        app_commands = {
            "browser": "xdg-open https://",
            "calculator": "gnome-calculator",
            "terminal": "gnome-terminal",
            "files": "nautilus",
            "settings": "gnome-control-center",
        }

        if target and target.lower() in app_commands:
            try:
                subprocess.Popen(
                    app_commands[target.lower()],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return {"status": "success", "message": f"Opened {target}"}
            except Exception as e:
                return {"status": "error", "message": f"Failed to open {target}: {e}"}

        return {
            "status": "partial",
            "message": f"Open action for '{target}' not fully implemented",
        }

    def _action_close(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'close' action.

        Args:
            target: What to close.
            params: Additional parameters.

        Returns:
            Execution result.
        """
        logger.debug(f"Closing: {target}")
        return {
            "status": "partial",
            "message": f"Close action for '{target}' not fully implemented",
        }

    def _action_click(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'click' action.

        Args:
            target: What to click.
            params: Additional parameters (x, y coordinates).

        Returns:
            Execution result.
        """
        logger.debug(f"Clicking: {target}")
        return {
            "status": "partial",
            "message": f"Click action for '{target}' not fully implemented",
        }

    def _action_type(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'type' action.

        Args:
            target: What to type.
            params: Additional parameters.

        Returns:
            Execution result.
        """
        logger.debug(f"Typing: {target}")
        return {
            "status": "partial",
            "message": f"Type action for '{target}' not fully implemented",
        }

    def _action_scroll(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'scroll' action.

        Args:
            target: Scroll direction (up, down, left, right).
            params: Additional parameters (amount).

        Returns:
            Execution result.
        """
        logger.debug(f"Scrolling: {target}")
        return {
            "status": "partial",
            "message": f"Scroll action for '{target}' not fully implemented",
        }

    def _action_search(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'search' action.

        Args:
            target: Search query.
            params: Additional parameters.

        Returns:
            Execution result.
        """
        logger.debug(f"Searching: {target}")

        if target:
            try:
                # Open default browser with search
                search_url = f"https://www.google.com/search?q={target.replace(' ', '+')}"
                subprocess.Popen(
                    f"xdg-open {search_url}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return {
                    "status": "success",
                    "message": f"Searching for '{target}'",
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to search: {e}",
                }

        return {"status": "error", "message": "No search query provided"}

    def _action_find(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 'find' action.

        Args:
            target: What to find on screen.
            params: Additional parameters.

        Returns:
            Execution result.
        """
        logger.debug(f"Finding: {target}")
        return {
            "status": "partial",
            "message": f"Find action for '{target}' not fully implemented",
        }

    def _action_unknown(
        self, target: Optional[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle unknown actions.

        Args:
            target: Action target.
            params: Additional parameters.

        Returns:
            Execution result indicating unknown action.
        """
        logger.warning(f"Unknown action requested for target: {target}")
        return {
            "status": "error",
            "message": "Unknown action",
        }

    def get_action_history(self, limit: int = 10) -> list:
        """Get recent action history.

        Args:
            limit: Maximum number of actions to return.

        Returns:
            List of recent actions.

        Example:
            >>> executor = ActionExecutor()
            >>> history = executor.get_action_history(5)
        """
        return self.action_history[-limit:]

    def clear_history(self) -> None:
        """Clear action history.

        Example:
            >>> executor = ActionExecutor()
            >>> executor.clear_history()
        """
        self.action_history = []
        logger.info("Action history cleared")

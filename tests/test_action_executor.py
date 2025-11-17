"""Unit tests for the ActionExecutor module."""

from unittest.mock import MagicMock, patch

import pytest

from bitdubber.core.action_executor import ActionExecutor
from bitdubber.utils.exceptions import ActionExecutionError


@pytest.fixture
def action_executor():
    """Provide an ActionExecutor instance for testing."""
    return ActionExecutor()


class TestActionExecutor:
    """Test cases for ActionExecutor class."""

    @pytest.mark.unit
    def test_initialization(self, action_executor):
        """Test ActionExecutor initialization."""
        assert action_executor is not None
        assert action_executor.action_history == []

    @pytest.mark.unit
    def test_execute_action_success(self, action_executor):
        """Test successful action execution."""
        result = action_executor.execute_action("search", "python")

        assert result["status"] == "success"
        assert len(action_executor.action_history) == 1

    @pytest.mark.unit
    def test_execute_action_with_params(self, action_executor):
        """Test action execution with parameters."""
        params = {"key": "value"}
        result = action_executor.execute_action("click", "button", params)

        assert "status" in result
        assert action_executor.action_history[0]["params"] == params

    @pytest.mark.unit
    def test_action_open_known_app(self, action_executor):
        """Test opening a known application."""
        with patch("subprocess.Popen") as mock_popen:
            result = action_executor._action_open("calculator", {})

            assert result["status"] == "success"
            assert "calculator" in result["message"].lower()
            mock_popen.assert_called_once()

    @pytest.mark.unit
    def test_action_open_unknown_app(self, action_executor):
        """Test opening an unknown application."""
        result = action_executor._action_open("unknown_app", {})

        assert result["status"] == "partial"

    @pytest.mark.unit
    def test_action_search_with_query(self, action_executor):
        """Test search action with query."""
        with patch("subprocess.Popen") as mock_popen:
            result = action_executor._action_search("python documentation", {})

            assert result["status"] == "success"
            mock_popen.assert_called_once()

    @pytest.mark.unit
    def test_action_search_without_query(self, action_executor):
        """Test search action without query."""
        result = action_executor._action_search(None, {})

        assert result["status"] == "error"

    @pytest.mark.unit
    def test_action_close(self, action_executor):
        """Test close action."""
        result = action_executor._action_close("window", {})

        assert result["status"] == "partial"

    @pytest.mark.unit
    def test_action_click(self, action_executor):
        """Test click action."""
        result = action_executor._action_click("button", {})

        assert result["status"] == "partial"

    @pytest.mark.unit
    def test_action_type(self, action_executor):
        """Test type action."""
        result = action_executor._action_type("hello world", {})

        assert result["status"] == "partial"

    @pytest.mark.unit
    def test_action_scroll(self, action_executor):
        """Test scroll action."""
        result = action_executor._action_scroll("down", {})

        assert result["status"] == "partial"

    @pytest.mark.unit
    def test_action_find(self, action_executor):
        """Test find action."""
        result = action_executor._action_find("text", {})

        assert result["status"] == "partial"

    @pytest.mark.unit
    def test_action_unknown(self, action_executor):
        """Test unknown action handling."""
        result = action_executor._action_unknown("something", {})

        assert result["status"] == "error"
        assert "unknown" in result["message"].lower()

    @pytest.mark.unit
    def test_get_action_history(self, action_executor):
        """Test getting action history."""
        # Execute some actions
        action_executor.execute_action("search", "test1")
        action_executor.execute_action("search", "test2")
        action_executor.execute_action("search", "test3")

        history = action_executor.get_action_history(limit=2)

        assert len(history) == 2
        assert history[0]["target"] == "test2"
        assert history[1]["target"] == "test3"

    @pytest.mark.unit
    def test_get_action_history_all(self, action_executor):
        """Test getting entire action history."""
        # Execute some actions
        for i in range(5):
            action_executor.execute_action("search", f"test{i}")

        history = action_executor.get_action_history(limit=10)

        assert len(history) == 5

    @pytest.mark.unit
    def test_clear_history(self, action_executor):
        """Test clearing action history."""
        action_executor.execute_action("search", "test")
        assert len(action_executor.action_history) == 1

        action_executor.clear_history()

        assert len(action_executor.action_history) == 0

    @pytest.mark.unit
    def test_action_history_contains_metadata(self, action_executor):
        """Test that action history contains metadata."""
        action_executor.execute_action("search", "test", {"param": "value"})

        history = action_executor.get_action_history()
        entry = history[0]

        assert "action" in entry
        assert "target" in entry
        assert "params" in entry
        assert "result" in entry
        assert "timestamp" in entry
        assert entry["action"] == "search"
        assert entry["target"] == "test"

    @pytest.mark.integration
    def test_multiple_actions_sequence(self, action_executor):
        """Test executing multiple actions in sequence."""
        actions = [
            ("search", "python"),
            ("search", "rust"),
            ("search", "go"),
        ]

        for action, target in actions:
            result = action_executor.execute_action(action, target)
            assert "status" in result

        assert len(action_executor.action_history) == 3

    @pytest.mark.unit
    def test_dispatch_action_case_insensitive(self, action_executor):
        """Test that action dispatch is case-insensitive."""
        result1 = action_executor.execute_action("SEARCH", "test")
        result2 = action_executor.execute_action("search", "test")

        assert result1["status"] == result2["status"]

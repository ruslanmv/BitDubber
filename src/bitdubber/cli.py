"""Command-line interface for BitDubber.

This module provides the CLI interface for running BitDubber.
"""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bitdubber import __version__
from bitdubber.config import get_settings
from bitdubber.core.action_executor import ActionExecutor
from bitdubber.core.screen_reader import ScreenReader
from bitdubber.core.voice_recognizer import VoiceRecognizer
from bitdubber.utils.exceptions import BitDubberError
from bitdubber.utils.logger import get_logger, setup_logging

console = Console()
logger = get_logger(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode",
)
@click.option(
    "--log-file",
    type=click.Path(path_type=Path),
    help="Path to log file",
)
def cli(debug: bool, log_file: Optional[Path]) -> None:
    """BitDubber - Desktop Assistant with Screen Reading and Voice Commands.

    Transform your desktop interaction with intelligent voice commands
    and screen-aware automation.
    """
    log_level = "DEBUG" if debug else "INFO"
    setup_logging(log_level=log_level, log_file=log_file)
    logger.info(f"BitDubber v{__version__} starting...")


@cli.command()
def info() -> None:
    """Display information about BitDubber."""
    settings = get_settings()

    info_panel = Panel(
        f"""[bold cyan]BitDubber[/bold cyan] v{__version__}

A cutting-edge desktop assistant combining screen-reading
capabilities with intelligent voice commands.

[bold]Author:[/bold] Ruslan Magana
[bold]Website:[/bold] https://ruslanmv.com
[bold]License:[/bold] Apache-2.0
        """,
        title="About BitDubber",
        border_style="cyan",
    )

    console.print(info_panel)

    # Settings table
    settings_table = Table(title="Current Settings", show_header=True)
    settings_table.add_column("Setting", style="cyan")
    settings_table.add_column("Value", style="green")

    settings_table.add_row("Debug Mode", str(settings.debug))
    settings_table.add_row("Log Level", settings.log_level)
    settings_table.add_row("OCR Language", settings.ocr_language)
    settings_table.add_row("Voice Language", settings.voice_language)
    settings_table.add_row("Screenshot Directory", str(settings.screenshot_dir))

    console.print(settings_table)


@cli.command()
@click.option(
    "--save",
    is_flag=True,
    help="Save screenshot to disk",
)
def screen_test() -> None:
    """Test screen reading functionality."""
    try:
        console.print("[cyan]Testing screen reader...[/cyan]")

        reader = ScreenReader()
        text = reader.capture_and_read(save_screenshot=save)

        console.print(Panel(
            text if text else "[yellow]No text detected[/yellow]",
            title="Screen Text",
            border_style="green",
        ))

        if reader.last_screenshot:
            console.print(f"[green]Screenshot saved to: {reader.last_screenshot}[/green]")

    except BitDubberError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cli.command()
def voice_test() -> None:
    """Test voice recognition functionality."""
    try:
        console.print("[cyan]Testing voice recognition...[/cyan]")
        console.print("[yellow]Available microphones:[/yellow]")

        recognizer = VoiceRecognizer()
        mics = recognizer.get_available_microphones()

        for idx, name in mics.items():
            console.print(f"  {idx}: {name}")

        console.print("\n[green]Speak a command...[/green]")
        recognizer.initialize_microphone()
        command = recognizer.listen_for_command()

        parsed = recognizer.parse_command(command)

        console.print(Panel(
            f"[bold]Raw:[/bold] {command}\n"
            f"[bold]Action:[/bold] {parsed['action']}\n"
            f"[bold]Target:[/bold] {parsed['target']}",
            title="Recognized Command",
            border_style="green",
        ))

    except BitDubberError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cli.command()
def run() -> None:
    """Run BitDubber in interactive mode."""
    try:
        console.print(Panel(
            "[bold cyan]BitDubber Interactive Mode[/bold cyan]\n\n"
            "Say commands to control your desktop.\n"
            "Say 'stop listening' to exit.",
            border_style="cyan",
        ))

        # Initialize components
        screen_reader = ScreenReader()
        voice_recognizer = VoiceRecognizer()
        action_executor = ActionExecutor()

        voice_recognizer.initialize_microphone()

        def handle_command(command: str) -> None:
            """Handle recognized voice command."""
            console.print(f"[yellow]Command:[/yellow] {command}")

            # Parse command
            parsed = voice_recognizer.parse_command(command)

            # Execute action
            try:
                result = action_executor.execute_action(
                    parsed["action"],
                    parsed["target"],
                    parsed.get("params", {}),
                )

                status_color = {
                    "success": "green",
                    "partial": "yellow",
                    "error": "red",
                }.get(result.get("status", "error"), "white")

                console.print(f"[{status_color}]{result.get('message', 'Done')}[/{status_color}]")

            except BitDubberError as e:
                console.print(f"[red]Action failed: {e}[/red]")

        # Start listening
        console.print("[green]Listening for commands...[/green]\n")
        voice_recognizer.listen_continuously(handle_command)

        console.print("\n[cyan]BitDubber stopped.[/cyan]")

    except BitDubberError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
    except KeyboardInterrupt:
        console.print("\n[cyan]BitDubber interrupted by user.[/cyan]")


def main() -> None:
    """Entry point for the CLI application."""
    cli()


if __name__ == "__main__":
    main()

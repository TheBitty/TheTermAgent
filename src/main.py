#!/usr/bin/env python3
"""
TermSage - AI-enhanced terminal emulator
Main entry point and terminal loop
"""

import os
import sys
import readline
from pathlib import Path

from command_handler import CommandHandler
from config import Config
from ollama_helper import OllamaHelper
from ui_utils import UIUtils, print_banner
from help_system import HelpSystem
from onboarding import OnboardingWizard
from command_registry import CommandRegistry, ChatHandler, AppState
from decorators import PathManager

# Constants
c_DEFAULT_PROMPT = "$ "
c_HISTORY_FILE = str(PathManager.get_history_file())


def setup_readline():
    """Configure readline for command history and tab completion"""
    # Enable tab completion
    readline.parse_and_bind("tab: complete")

    # Load history if it exists
    try:
        readline.read_history_file(c_HISTORY_FILE)
    except FileNotFoundError:
        # Create history file directory
        Path(c_HISTORY_FILE).parent.mkdir(parents=True, exist_ok=True)

    # Set history length
    readline.set_history_length(1000)


def save_history():
    """Save command history on exit"""
    try:
        readline.write_history_file(c_HISTORY_FILE)
    except Exception:
        pass


def get_prompt(ui_utils, mode="normal"):
    """Generate the command prompt with current directory and mode indicator"""
    cwd = os.getcwd()
    home = str(Path.home())

    # Replace home directory with ~
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]

    # Add mode indicator
    if mode == "chat":
        return ui_utils.prompt(f"[Chat] {cwd} $ ")
    else:
        return ui_utils.prompt(f"{cwd} $ ")


def ensure_root_startup():
    """Ensure the terminal starts with root privileges if needed"""
    import subprocess

    # Check if we're already running as root
    if os.geteuid() != 0:
        # We're not root, need to restart with sudo
        print("Starting TermSage with root privileges...")
        try:
            # Get the current script path
            script_path = os.path.abspath(__file__)
            # Restart with sudo
            subprocess.run(["sudo", "python3", script_path] + sys.argv[1:])
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nCancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"Failed to start with root privileges: {e}")
            print("Continuing without root privileges...")


def main():
    """Main terminal loop"""
    # Initialize components
    config = Config()
    
    # Ensure root startup if configured
    if config.is_sudo_enabled():
        ensure_root_startup()

    # Initialize remaining components
    command_handler = CommandHandler()
    ollama = OllamaHelper(config)
    ui = UIUtils()
    help_system = HelpSystem(config, ollama)
    onboarding = OnboardingWizard(config)

    # Initialize command registry and state
    state = AppState()
    command_registry = CommandRegistry(ui, help_system, onboarding, ollama, config)
    command_registry.set_state(state)
    chat_handler = ChatHandler(ui, ollama, state)

    # Setup readline for history
    setup_readline()

    # Show enhanced banner
    print_banner()

    # Check AI status and show with colors
    if config.is_ai_enabled() and ollama.is_available():
        print(ui.success(f"AI ready with model: {ollama.current_model}"))
    elif config.is_ai_enabled():
        print(ui.warning("AI enabled but Ollama not running. Start with: ollama serve"))
    else:
        print(ui.info("AI disabled in config"))

    # Check for first-time setup
    if onboarding.should_run_setup():
        if not config.get("setup.auto_completed", False):
            # Run quick auto-setup first
            onboarding.quick_setup()
            config.set("setup.auto_completed", True)
            config.save()

        print(f"\n{ui.info('First time using TermSage?')}")
        response = input(ui.prompt("Would you like to run the setup wizard? (Y/n): ")).strip().lower()
        if not response or response.startswith("y"):
            onboarding.run_setup()

    # Show first-run help if needed
    if help_system.should_show_first_run_help():
        help_system.show_first_run_prompt()

    # Main terminal loop
    while True:
        try:
            # Show contextual tips occasionally
            if state.command_count > 0 and state.command_count % 10 == 0:
                tips = help_system.get_contextual_tips(os.getcwd(), state.get_recent_commands())
                for tip in tips:
                    print(tip)

            # Get user input with enhanced prompt
            mode = "chat" if state.chat_mode else "normal"
            prompt = get_prompt(ui, mode)
            user_input = input(prompt).strip()

            # Skip empty input
            if not user_input:
                continue

            # Track command for contextual help
            state.add_command(user_input)

            # Handle chat mode
            if state.chat_mode:
                if not chat_handler.handle_chat_input(user_input):
                    # Chat handler returned False, exit chat mode
                    continue
                else:
                    continue

            # Handle built-in commands using registry
            result = command_registry.execute(user_input)
            if result is not None:
                if not result:
                    # Command returned False, exit the loop
                    break
                else:
                    # Command was handled, continue loop
                    continue

            # Execute normal command with enhanced error handling
            try:
                cmd_result = command_handler.execute(user_input)
                if cmd_result and hasattr(cmd_result, "returncode") and cmd_result.returncode != 0:
                    # Command failed - offer AI help if available
                    if config.get("ai.help_on_error", True) and ollama.is_available():
                        print(ui.info("Command failed. Getting AI suggestions..."))
                        try:
                            error_help = ollama.get_error_help(
                                user_input, cmd_result.stderr if hasattr(cmd_result, "stderr") else ""
                            )
                            print(ui.ai_response(error_help))
                        except Exception:
                            pass
            except Exception as e:
                print(ui.error(f"Command execution error: {e}"))
                # Offer help for command not found
                if "command not found" in str(e).lower() or "not recognized" in str(e).lower():
                    suggestions = help_system.suggest_commands(user_input.split()[0] if user_input else "", os.getcwd())
                    if suggestions:
                        print(ui.info("Did you mean: " + ", ".join(suggestions[:3])))

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n" + ui.dim("^C"))
            if state.chat_mode:
                state.chat_mode = False
                print(ui.info("Exited chat mode"))
            continue

        except EOFError:
            # Handle Ctrl+D
            print("\n" + ui.success("Goodbye!"))
            break

        except Exception as e:
            print(ui.error(f"Unexpected error: {e}"))
            continue

    # Save history before exiting
    save_history()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ui = UIUtils()
        print("\n" + ui.success("Goodbye!"))
        save_history()
        sys.exit(0)


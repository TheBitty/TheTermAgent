"""
Command Registry - Centralized command handling for TermSage
"""

from typing import Dict, Callable, Optional
from ui_utils import UIUtils, show_help, LoadingIndicator
import os


class CommandRegistry:
    """Registry for handling built-in TermSage commands"""

    def __init__(self, ui: UIUtils, help_system, onboarding, ollama, config):
        self.ui = ui
        self.help_system = help_system
        self.onboarding = onboarding
        self.ollama = ollama
        self.config = config
        self.state = None  # Will be set by main

        # Register all commands
        self.commands: Dict[str, Callable] = {
            "/exit": self.handle_exit,
            "exit": self.handle_exit,  # Map regular exit to /exit
            "help": self.handle_help,
            "/tutorial": self.handle_tutorial,
            "/setup": self.handle_setup,
            "/chat": self.handle_chat,
            "clear": self.handle_clear,
            "/models": self.handle_models,
            "/config": self.handle_config,
        }

        # Commands that require patterns (like /model <name>)
        self.pattern_commands = {
            "/model ": self.handle_model_switch,
        }

    def set_state(self, state):
        """Set the application state reference"""
        self.state = state

    def execute(self, command: str) -> Optional[bool]:
        """
        Execute a command if it's registered

        Args:
            command: The command string to execute

        Returns:
            True if command was handled and should continue loop
            False if command was handled and should break loop
            None if command was not handled
        """
        command_lower = command.lower()

        # Check exact matches first
        if command_lower in self.commands:
            return self.commands[command_lower]()

        # Check pattern matches
        for pattern, handler in self.pattern_commands.items():
            if command.startswith(pattern):
                return handler(command)

        # Check for help pattern (ends with ?)
        if command.endswith("?"):
            return self.handle_help_request(command)

        # Command not handled
        return None

    def handle_exit(self) -> bool:
        """Handle exit command"""
        print(self.ui.success("Goodbye!"))
        return False  # Break the loop

    def handle_help(self) -> bool:
        """Handle help command"""
        show_help()
        return True

    def handle_tutorial(self) -> bool:
        """Handle tutorial command"""
        self.help_system.run_interactive_tutorial()
        return True

    def handle_setup(self) -> bool:
        """Handle setup command"""
        self.onboarding.run_setup()
        return True

    def handle_chat(self) -> bool:
        """Handle chat mode toggle"""
        if self.state:
            self.state.toggle_chat_mode()
            print(self.ui.info("Entered chat mode - Ask questions in natural language"))
            print(self.ui.dim("Type /exit to return to normal mode"))
        return True

    def handle_clear(self) -> bool:
        """Handle clear screen command"""
        os.system("clear" if os.name != "nt" else "cls")
        return True

    def handle_models(self) -> bool:
        """Handle models list command"""
        if self.ollama.is_available():
            self.ollama.list_models()
        else:
            print(self.ui.warning("Ollama not available"))
        return True

    def handle_config(self) -> bool:
        """Handle config display command"""
        self.config.show_config()
        return True

    def handle_model_switch(self, command: str) -> bool:
        """Handle model switch command"""
        model_name = command[7:].strip()  # Remove "/model "
        if model_name:
            if self.ollama.is_available():
                self.ollama.switch_model(model_name)
            else:
                print(self.ui.warning("Ollama not available"))
        else:
            print(self.ui.error("Usage: /model <model_name>"))
        return True

    def handle_help_request(self, command: str) -> bool:
        """Handle command help requests (command?)"""
        command_name = command[:-1].strip()  # Remove the ?
        if command_name:
            if self.ollama.is_available():
                # Only show loading indicator if response is not cached
                indicator = None
                if not self.ollama.is_help_cached(command_name):
                    indicator = LoadingIndicator("Getting help", self.ui)
                    indicator.start()

                try:
                    help_text = self.ollama.get_help(command_name)
                    if indicator:
                        indicator.stop()
                    print(self.ui.ai_response(help_text))
                except Exception as e:
                    if indicator:
                        indicator.stop()
                    print(self.ui.error(f"Error getting help: {e}"))
            else:
                print(self.ui.warning(f"AI not available for help. Try: man {command_name}"))
        else:
            print(self.ui.info("Usage: <command>? (e.g., git?, docker?, ls?)"))
        return True


class ChatHandler:
    """Specialized handler for chat mode commands"""

    def __init__(self, ui: UIUtils, ollama, state):
        self.ui = ui
        self.ollama = ollama
        self.state = state

        self.chat_commands = {
            "/exit": self.exit_chat,
            "/clear": self.clear_chat,
            "/help": self.help_chat,
        }

    def handle_chat_input(self, user_input: str) -> bool:
        """
        Handle input while in chat mode

        Returns:
            True to continue in chat mode, False to exit chat mode
        """
        # Check for chat-specific commands
        if user_input.lower() in self.chat_commands:
            return self.chat_commands[user_input.lower()]()

        # Handle regular chat interaction
        if self.ollama.is_available():
            indicator = LoadingIndicator("Thinking", self.ui)
            indicator.start()
            try:
                response = self.ollama.chat(user_input)
                indicator.stop()
                print(self.ui.ai_response(response))
            except Exception as e:
                indicator.stop()
                print(self.ui.error(f"Chat error: {e}"))
        else:
            print(self.ui.warning("AI not available for chat mode"))

        return True  # Stay in chat mode

    def exit_chat(self) -> bool:
        """Exit chat mode"""
        if self.state:
            self.state.chat_mode = False
        print(self.ui.info("Exited chat mode"))
        return False

    def clear_chat(self) -> bool:
        """Clear chat context"""
        print(self.ui.info("Chat context cleared"))
        return True

    def help_chat(self) -> bool:
        """Show chat mode help"""
        print(self.ui.info("Chat mode - Ask questions in natural language"))
        print(self.ui.dim("Commands: /exit (exit chat), /clear (clear context), /help (this message)"))
        return True


class AppState:
    """Centralized application state management"""

    def __init__(self):
        self.chat_mode = False
        self.recent_commands = []
        self.command_count = 0

    def add_command(self, command: str):
        """Add a command to history"""
        self.recent_commands.append(command)
        if len(self.recent_commands) > 50:  # Keep last 50 commands
            self.recent_commands.pop(0)
        self.command_count += 1

    def toggle_chat_mode(self):
        """Toggle chat mode and return new state"""
        self.chat_mode = not self.chat_mode
        return self.chat_mode

    def get_recent_commands(self, limit: int = 10) -> list:
        """Get recent commands up to limit"""
        return self.recent_commands[-limit:] if self.recent_commands else []


"""
Help System - Interactive tutorials and feature discovery for TermSage
"""

import os
from pathlib import Path
from ui_utils import UIUtils


class HelpSystem:
    """Manages help, tutorials, and feature discovery"""

    def __init__(self, config=None, ollama=None):
        self.ui = UIUtils()
        self.config = config
        self.ollama = ollama
        self.tutorial_completed = self._check_tutorial_status()

    def _check_tutorial_status(self) -> bool:
        """Check if user has completed the tutorial"""
        marker_file = Path.home() / ".termsage" / ".tutorial_completed"
        return marker_file.exists()

    def _mark_tutorial_complete(self):
        """Mark tutorial as completed"""
        marker_file = Path.home() / ".termsage" / ".tutorial_completed"
        marker_file.parent.mkdir(parents=True, exist_ok=True)
        marker_file.touch()
        self.tutorial_completed = True

    def should_show_first_run_help(self) -> bool:
        """Check if we should show first-run help"""
        return not self.tutorial_completed

    def show_first_run_prompt(self):
        """Show first-run tutorial prompt"""
        print(f"\n{self.ui.info('First time using TermSage?')}")
        print(f"{self.ui.dim('• Type')} {self.ui.command('/tutorial')} {self.ui.dim('for an interactive walkthrough')}")
        print(f"{self.ui.dim('• Type')} {self.ui.command('help')} {self.ui.dim('for a complete feature guide')}")
        print(f"{self.ui.dim('• Try')} {self.ui.command('git?')} {self.ui.dim('to see AI help in action')}")
        print()

    def run_interactive_tutorial(self):
        """Run the interactive tutorial"""
        print(f"\n{self.ui.colorize('🎓 TermSage Interactive Tutorial', self.ui.Color.BRIGHT_WHITE, bold=True)}")
        print(f"{self.ui.colorize('═' * 50, self.ui.Color.BRIGHT_CYAN)}\n")

        steps = [
            self._tutorial_welcome,
            self._tutorial_basic_commands,
            self._tutorial_ai_help,
            self._tutorial_chat_mode,
            self._tutorial_error_handling,
            self._tutorial_configuration,
            self._tutorial_completion,
        ]

        for i, step in enumerate(steps, 1):
            print(f"{self.ui.colorize(f'Step {i}/{len(steps)}', self.ui.Color.BRIGHT_YELLOW, bold=True)}")
            if not step():
                print(f"\n{self.ui.warning('Tutorial interrupted. Type /tutorial to resume anytime.')}")
                return

            if i < len(steps):
                self._wait_for_continue()

        self._mark_tutorial_complete()
        print(f"\n{self.ui.success('Tutorial completed! You\'re ready to use TermSage effectively.')}")

    def _wait_for_continue(self):
        """Wait for user to continue tutorial"""
        try:
            input(f"\n{self.ui.dim('Press Enter to continue, or Ctrl+C to exit tutorial...')}")
            print()
        except KeyboardInterrupt:
            return False
        return True

    def _tutorial_welcome(self) -> bool:
        """Tutorial step 1: Welcome and overview"""
        print(f"{self.ui.info('Welcome to TermSage!')}")
        print("TermSage is your regular terminal enhanced with AI assistance.")
        print("Let's explore the key features that will make you more productive.\n")

        print(f"{self.ui.colorize('What you\'ll learn:', self.ui.Color.BRIGHT_WHITE, bold=True)}")
        print("• How to get AI help for any command")
        print("• Using chat mode for complex questions")
        print("• Automatic error analysis and suggestions")
        print("• Configuration and customization")
        return True

    def _tutorial_basic_commands(self) -> bool:
        """Tutorial step 2: Basic enhanced commands"""
        print(f"{self.ui.colorize('🔧 Enhanced Commands', self.ui.Color.BRIGHT_BLUE, bold=True)}")
        print("TermSage works like any terminal, but with AI superpowers.\n")

        print(f"{self.ui.command('Try this: ls')} {self.ui.dim('(works exactly like normal)')}")
        self._demo_command("ls")

        print(f"\n{self.ui.command('Now try: ls?')} {self.ui.dim('(adds ? for AI help)')}")
        if self.ollama and self.ollama.is_available():
            print(f"{self.ui.ai_response('AI explains: ls lists directory contents. Common options:')}")
            print(f"{self.ui.ai_response('  -l : detailed list with permissions and dates')}")
            print(f"{self.ui.ai_response('  -a : show hidden files (starting with .)')}")
            print(f"{self.ui.ai_response('  -h : human-readable file sizes')}")
        else:
            print(f"{self.ui.warning('AI not available, but this is where you\'d see helpful explanations!')}")

        print(f"\n{self.ui.success('Key insight: Add ? to ANY command for instant help!')}")
        return True

    def _tutorial_ai_help(self) -> bool:
        """Tutorial step 3: AI help system"""
        print(f"{self.ui.colorize('🤖 AI Help System', self.ui.Color.BRIGHT_BLUE, bold=True)}")
        print("Get contextual help for any command, even complex ones.\n")

        examples = [
            ("git?", "Git version control help"),
            ("docker?", "Docker container management"),
            ("tar?", "Archive and compression"),
            ("ffmpeg?", "Video/audio processing"),
            ("systemctl?", "Service management"),
        ]

        print(f"{self.ui.colorize('Popular examples:', self.ui.Color.BRIGHT_WHITE, bold=True)}")
        for cmd, desc in examples:
            print(f"  {self.ui.command(cmd):<12} {self.ui.dim('→')} {desc}")

        print(f"\n{self.ui.info('The AI understands your current directory and provides relevant examples.')}")
        print(f"{self.ui.dim('For instance, in a git repo, git? will show repository-specific advice.')}")
        return True

    def _tutorial_chat_mode(self) -> bool:
        """Tutorial step 4: Chat mode"""
        print(f"{self.ui.colorize('💬 Chat Mode', self.ui.Color.BRIGHT_BLUE, bold=True)}")
        print("For complex questions or troubleshooting, use chat mode.\n")

        print(f"{self.ui.command('/chat')} {self.ui.dim('→ Start conversational AI mode')}")
        print("\nIn chat mode, you can ask things like:")
        print(f"• {self.ui.dim('\"How do I find files larger than 100MB?\"')}")
        print(f"• {self.ui.dim('\"Explain this error message: permission denied\"')}")
        print(f"• {self.ui.dim('\"What\'s the best way to monitor CPU usage?\"')}")
        print(f"• {self.ui.dim('\"Help me write a bash script to backup files\"')}")

        print(f"\n{self.ui.info('Chat mode maintains context, so you can have natural conversations.')}")
        print(f"{self.ui.dim('Use /exit to return to normal terminal mode.')}")
        return True

    def _tutorial_error_handling(self) -> bool:
        """Tutorial step 5: Error handling"""
        print(f"{self.ui.colorize('🆘 Smart Error Handling', self.ui.Color.BRIGHT_BLUE, bold=True)}")
        print("When commands fail, TermSage automatically provides helpful suggestions.\n")

        print(f"{self.ui.error('Example: command not found: dockerr')}")
        print(f"{self.ui.ai_response('Did you mean: docker')}")
        print(f"{self.ui.ai_response('Or try: sudo apt install docker.io')}")

        print(f"\n{self.ui.error('Example: Permission denied')}")
        print(f"{self.ui.ai_response('Try: sudo <your-command>')}")
        print(f"{self.ui.ai_response('Or check file permissions with: ls -la')}")

        print(f"\n{self.ui.success('No more searching online for error solutions!')}")
        return True

    def _tutorial_configuration(self) -> bool:
        """Tutorial step 6: Configuration"""
        print(f"{self.ui.colorize('⚙️  Configuration', self.ui.Color.BRIGHT_BLUE, bold=True)}")
        print("Customize TermSage to fit your workflow.\n")

        print(f"{self.ui.command('/config')} {self.ui.dim('→ View current settings')}")
        print(f"{self.ui.command('/models')} {self.ui.dim('→ List available AI models')}")
        print(f"{self.ui.command('/model llama2')} {self.ui.dim('→ Switch AI model')}")

        print(
            f"\n{self.ui.colorize('Configuration file:', self.ui.Color.BRIGHT_WHITE, bold=True)} {self.ui.dim('~/.termsage/config.json')}"
        )
        print(
            f"{self.ui.colorize('History file:', self.ui.Color.BRIGHT_WHITE, bold=True)} {self.ui.dim('~/.termsage/history')}"
        )

        if self.config:
            print(f"\n{self.ui.info(f'Current AI model: {self.config.get_ollama_model()}')}")
            print(f"{self.ui.info(f'AI enabled: {self.config.is_ai_enabled()}')}")

        return True

    def _tutorial_completion(self) -> bool:
        """Tutorial step 7: Completion"""
        print(f"{self.ui.colorize('🎉 You\'re All Set!', self.ui.Color.BRIGHT_GREEN, bold=True)}")
        print("Here's a quick reference for daily use:\n")

        reference = [
            ("help", "Show complete help"),
            ("command?", "Get AI help for any command"),
            ("/chat", "Start AI conversation"),
            ("/tutorial", "Replay this tutorial"),
            ("clear", "Clear screen"),
            ("/exit", "Exit TermSage"),
        ]

        print(f"{self.ui.colorize('Quick Reference:', self.ui.Color.BRIGHT_WHITE, bold=True)}")
        for cmd, desc in reference:
            print(f"  {self.ui.command(cmd):<12} {self.ui.dim('→')} {desc}")

        print(f"\n{self.ui.success('Pro tip: TermSage learns from your usage patterns!')}")
        print(f"{self.ui.dim('The more you use it, the better suggestions you\'ll get.')}")
        return True

    def _demo_command(self, command: str) -> str:
        """Demonstrate a command execution"""
        # This is a simplified demo - in real implementation,
        # you'd integrate with the actual command handler
        if command == "ls":
            return "file1.txt  file2.py  directory/  README.md"
        return f"[Demo output for: {command}]"

    def get_contextual_tips(self, current_dir: str, recent_commands: list) -> list:
        """Generate contextual tips based on current context"""
        tips = []

        # Directory-based tips
        if os.path.exists(os.path.join(current_dir, ".git")):
            tips.append(f"{self.ui.info('Git repository detected!')} Try: {self.ui.command('git?')} for git help")

        if os.path.exists(os.path.join(current_dir, "package.json")):
            tips.append(f"{self.ui.info('Node.js project detected!')} Try: {self.ui.command('npm?')} for npm help")

        if os.path.exists(os.path.join(current_dir, "Dockerfile")):
            tips.append(f"{self.ui.info('Docker project detected!')} Try: {self.ui.command('docker?')} for docker help")

        if os.path.exists(os.path.join(current_dir, "requirements.txt")):
            tips.append(f"{self.ui.info('Python project detected!')} Try: {self.ui.command('pip?')} for pip help")

        # Command-based tips
        if recent_commands:
            last_cmd = recent_commands[-1] if recent_commands else ""
            if "git" in last_cmd and not last_cmd.endswith("?"):
                tips.append(
                    f"{self.ui.dim('Hint:')} Add {self.ui.command('?')} to git commands for help (e.g., {self.ui.command('git?')})"
                )

        return tips[:2]  # Limit to 2 tips to avoid spam

    def suggest_commands(self, partial_command: str, current_dir: str) -> list:
        """Suggest commands based on partial input and context"""
        suggestions = []

        # Basic command suggestions
        common_commands = [
            "ls",
            "cd",
            "pwd",
            "mkdir",
            "rm",
            "cp",
            "mv",
            "grep",
            "find",
            "git",
            "docker",
            "npm",
            "pip",
            "python",
            "node",
            "vim",
            "nano",
            "tar",
            "curl",
            "wget",
            "ssh",
            "scp",
            "systemctl",
            "ps",
            "top",
        ]

        # Filter commands that start with partial input
        matching_commands = [cmd for cmd in common_commands if cmd.startswith(partial_command)]

        # Add help suffix suggestions
        if partial_command and not partial_command.endswith("?"):
            suggestions.append(f"{partial_command}?")

        suggestions.extend(matching_commands[:5])  # Limit suggestions

        return suggestions


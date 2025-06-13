"""
Onboarding Wizard - First-time setup and configuration for TermSage
"""

import subprocess
from pathlib import Path
from ui_utils import UIUtils, LoadingIndicator


class OnboardingWizard:
    """Guides users through first-time setup"""

    def __init__(self, config):
        self.config = config
        self.ui = UIUtils()
        self.setup_completed = False

    def run_setup(self):
        """Run the complete onboarding process"""
        print(f"\n{self.ui.colorize('🚀 TermSage Setup Wizard', self.ui.Color.BRIGHT_WHITE, bold=True)}")
        print(f"{self.ui.colorize('═' * 50, self.ui.Color.BRIGHT_CYAN)}\n")

        print(self.ui.info("Welcome! Let's get TermSage configured for you."))
        print(f"{self.ui.dim('This will only take a few minutes.')}\n")

        steps = [
            ("System Check", self._check_system),
            ("AI Configuration", self._setup_ai),
            ("Terminal Preferences", self._setup_terminal),
            ("Test Features", self._test_features),
            ("Final Setup", self._finalize_setup),
        ]

        for i, (step_name, step_func) in enumerate(steps, 1):
            print(f"{self.ui.colorize(f'Step {i}/{len(steps)}: {step_name}', self.ui.Color.BRIGHT_YELLOW, bold=True)}")

            try:
                if not step_func():
                    print(f"\n{self.ui.warning('Setup interrupted. You can run this again anytime with /setup')}")
                    return False
            except KeyboardInterrupt:
                print(f"\n{self.ui.warning('Setup cancelled. Run /setup to try again.')}")
                return False

            if i < len(steps):
                self._wait_for_continue()

        self.setup_completed = True
        print(f"\n{self.ui.success('🎉 Setup complete! TermSage is ready to use.')}")
        return True

    def _wait_for_continue(self):
        """Wait for user to continue"""
        try:
            input(f"\n{self.ui.dim('Press Enter to continue...')}")
            print()
        except KeyboardInterrupt:
            return False
        return True

    def _check_system(self) -> bool:
        """Check system compatibility and requirements"""
        print(f"{self.ui.info('Checking system compatibility...')}\n")

        checks = [
            ("Python version", self._check_python),
            ("Terminal capabilities", self._check_terminal),
            ("Required packages", self._check_packages),
            ("Directory permissions", self._check_permissions),
        ]

        all_passed = True
        for check_name, check_func in checks:
            result, message = check_func()
            if result:
                print(f"{self.ui.success(f'{check_name}: {message}')}")
            else:
                print(f"{self.ui.error(f'{check_name}: {message}')}")
                all_passed = False

        if not all_passed:
            print(f"\n{self.ui.warning('Some system checks failed. TermSage may not work optimally.')}")
            response = input(f"{self.ui.dim('Continue anyway? (y/N): ')}")
            return response.lower().startswith("y")

        print(f"\n{self.ui.success('System checks passed!')}")
        return True

    def _check_python(self) -> tuple:
        """Check Python version"""
        import sys

        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {version.major}.{version.minor} (3.8+ required)"

    def _check_terminal(self) -> tuple:
        """Check terminal capabilities"""
        if self.ui.colors_enabled:
            return True, "Colors and formatting supported"
        else:
            return False, "Basic terminal (limited formatting)"

    def _check_packages(self) -> tuple:
        """Check required packages"""
        try:
            import requests

            return True, "All required packages available"
        except ImportError:
            return False, "Missing required packages (run: pip install requests)"

    def _check_permissions(self) -> tuple:
        """Check directory permissions"""
        config_dir = Path.home() / ".termsage"
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            test_file = config_dir / ".test"
            test_file.touch()
            test_file.unlink()
            return True, f"Can write to {config_dir}"
        except Exception as e:
            return False, f"Cannot write to {config_dir}: {e}"

    def _setup_ai(self) -> bool:
        """Configure AI settings"""
        print(f"{self.ui.info('Setting up AI integration...')}\n")

        # Check if Ollama is available
        ollama_available = self._check_ollama()

        if ollama_available:
            print(f"{self.ui.success('Ollama detected and running!')}")
            models = self._get_available_models()

            if models:
                print(f"\n{self.ui.info('Available AI models:')}")
                for i, model in enumerate(models, 1):
                    print(f"  {i}. {model}")

                while True:
                    try:
                        choice = input(
                            f"\n{self.ui.prompt('Select a model (1-{len(models)}) or press Enter for default: ')}"
                        )
                        if not choice:
                            # Use default (first model)
                            selected_model = models[0]
                            break

                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(models):
                            selected_model = models[choice_idx]
                            break
                        else:
                            print(f"{self.ui.error('Invalid choice. Please try again.')}")
                    except ValueError:
                        print(f"{self.ui.error('Please enter a number.')}")
                    except KeyboardInterrupt:
                        return False

                self.config.set("ai.model", selected_model)
                self.config.set("ai.enabled", True)
                print(f"{self.ui.success(f'AI configured with model: {selected_model}')}")
            else:
                print(f"{self.ui.warning('No AI models found.')}")
                if self._ask_yes_no("Would you like to install a recommended model?"):
                    self._install_default_model()
        else:
            print(f"{self.ui.warning('Ollama not detected.')}")
            print(self.ui.info("TermSage can work without AI, but you'll miss many features."))

            if self._ask_yes_no("Would you like to install Ollama?"):
                self._guide_ollama_installation()
            else:
                self.config.set("ai.enabled", False)
                print(f"{self.ui.info('AI features disabled. You can enable them later.')}")

        return True

    def _check_ollama(self) -> bool:
        """Check if Ollama is available"""
        try:
            import requests

            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            return response.status_code == 200
        except Exception:
            return False

    def _get_available_models(self) -> list:
        """Get list of available Ollama models"""
        try:
            import requests

            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except Exception:
            pass
        return []

    def _install_default_model(self):
        """Guide user through installing a default model"""
        print(f"\n{self.ui.info('Installing llama3.2:1b (small, fast model)...')}")
        print(f"{self.ui.dim('This may take a few minutes depending on your internet connection.')}")

        try:
            process = subprocess.Popen(
                ["ollama", "pull", "llama3.2:1b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            print(f"{self.ui.dim('Downloading... (you can continue using TermSage in another terminal)')}")
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print(f"{self.ui.success('Model installed successfully!')}")
                self.config.set("ai.model", "llama3.2:1b")
                self.config.set("ai.enabled", True)
            else:
                print(f"{self.ui.error('Failed to install model.')}")
                print(f"{self.ui.dim('You can install manually later with: ollama pull llama3.2:1b')}")
        except FileNotFoundError:
            print(f"{self.ui.error('Ollama command not found. Please install Ollama first.')}")

    def _guide_ollama_installation(self):
        """Guide user through Ollama installation"""
        print(f"\n{self.ui.info('Ollama Installation Guide:')}")

        # Detect OS and provide appropriate instructions
        import platform

        system = platform.system().lower()

        if system == "linux":
            print(f"  {self.ui.command('curl -fsSL https://ollama.com/install.sh | sh')}")
        elif system == "darwin":  # macOS
            print(f"  {self.ui.info('Download from: https://ollama.com/download')}")
            print(f"  {self.ui.dim('Or with Homebrew:')} {self.ui.command('brew install ollama')}")
        elif system == "windows":
            print(f"  {self.ui.info('Download from: https://ollama.com/download')}")
        else:
            print(f"  {self.ui.info('Visit: https://ollama.com/download')}")

        print(f"\n{self.ui.dim('After installation, start Ollama with:')} {self.ui.command('ollama serve')}")
        print(f"{self.ui.dim('Then install a model:')} {self.ui.command('ollama pull llama3.2:1b')}")

        if self._ask_yes_no("Have you installed Ollama and would like to test it?"):
            if self._check_ollama():
                print(f"{self.ui.success('Ollama is working!')}")
                self.config.set("ai.enabled", True)
            else:
                print(self.ui.warning("Ollama not detected. Make sure it's running with: ollama serve"))

    def _setup_terminal(self) -> bool:
        """Configure terminal preferences"""
        print(f"{self.ui.info('Configuring terminal preferences...')}\n")

        # History size
        print(f"{self.ui.dim('Command history settings:')}")
        current_size = self.config.get("terminal.history_size", 1000)

        while True:
            try:
                size_input = input(f"{self.ui.prompt(f'History size [{current_size}]: ')}")
                if not size_input:
                    history_size = current_size
                    break

                history_size = int(size_input)
                if history_size > 0:
                    break
                else:
                    print(f"{self.ui.error('Please enter a positive number.')}")
            except ValueError:
                print(f"{self.ui.error('Please enter a valid number.')}")
            except KeyboardInterrupt:
                return False

        self.config.set("terminal.history_size", history_size)

        # Auto error help
        auto_help = self._ask_yes_no("Enable automatic AI error analysis?", default=True)
        self.config.set("ai.help_on_error", auto_help)

        print(f"{self.ui.success('Terminal preferences configured!')}")
        return True

    def _test_features(self) -> bool:
        """Test key features"""
        print(f"{self.ui.info('Testing TermSage features...')}\n")

        # Test basic command
        print(f"{self.ui.dim('Testing command execution...')}")
        print(f"  {self.ui.command('ls')} → ", end="")
        try:
            result = subprocess.run(["ls"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"{self.ui.success('OK')}")
            else:
                print(f"{self.ui.warning('Command failed but execution works')}")
        except Exception as e:
            print(f"{self.ui.error(f'Failed: {e}')}")

        # Test AI if available
        if self.config.get("ai.enabled", False) and self._check_ollama():
            print(f"{self.ui.dim('Testing AI integration...')}")
            print(f"  {self.ui.command('AI help test')} → ", end="")

            indicator = LoadingIndicator("Testing AI", self.ui)
            indicator.start()

            try:
                import requests

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.config.get("ai.model", "llama3.2:1b"),
                        "prompt": "Say 'Hello' if you can understand this.",
                        "stream": False,
                        "options": {"num_predict": 10},
                    },
                    timeout=15,
                )
                indicator.stop()

                if response.status_code == 200:
                    print(f"{self.ui.success('OK')}")
                else:
                    print(f"{self.ui.warning('AI responded but with issues')}")
            except Exception as e:
                indicator.stop()
                print(f"{self.ui.error(f'Failed: {e}')}")

        print(f"\n{self.ui.success('Feature testing complete!')}")
        return True

    def _finalize_setup(self) -> bool:
        """Finalize setup and save configuration"""
        print(f"{self.ui.info('Finalizing setup...')}")

        # Save configuration
        self.config.save()

        # Create completion marker
        marker_file = Path.home() / ".termsage" / ".setup_completed"
        marker_file.touch()

        # Show summary
        print(f"\n{self.ui.colorize('Setup Summary:', self.ui.Color.BRIGHT_WHITE, bold=True)}")
        print(f"  AI Enabled: {self.ui.success('Yes') if self.config.get('ai.enabled') else self.ui.warning('No')}")
        if self.config.get("ai.enabled"):
            print(f"  AI Model: {self.config.get('ai.model', 'Not set')}")
        print(f"  History Size: {self.config.get('terminal.history_size', 1000)}")
        print(
            f"  Error Help: {self.ui.success('Enabled') if self.config.get('ai.help_on_error') else self.ui.warning('Disabled')}"
        )

        print(f"\n{self.ui.info('Quick tips to get started:')}")
        print(f"  • Type {self.ui.command('help')} for a complete guide")
        print(f"  • Try {self.ui.command('git?')} to see AI help in action")
        print(f"  • Use {self.ui.command('/chat')} for AI conversations")
        print(f"  • Run {self.ui.command('/tutorial')} for an interactive walkthrough")

        return True

    def _ask_yes_no(self, question: str, default: bool = None) -> bool:
        """Ask a yes/no question"""
        if default is True:
            prompt = f"{question} (Y/n): "
        elif default is False:
            prompt = f"{question} (y/N): "
        else:
            prompt = f"{question} (y/n): "

        while True:
            try:
                response = input(self.ui.prompt(prompt)).strip().lower()

                if not response and default is not None:
                    return default
                elif response in ["y", "yes"]:
                    return True
                elif response in ["n", "no"]:
                    return False
                else:
                    print(f"{self.ui.error('Please answer y or n.')}")
            except KeyboardInterrupt:
                return False

    def should_run_setup(self) -> bool:
        """Check if setup should be run"""
        marker_file = Path.home() / ".termsage" / ".setup_completed"
        return not marker_file.exists()

    def detect_and_configure_ai(self):
        """Auto-detect and configure AI settings"""
        if self._check_ollama():
            models = self._get_available_models()
            if models:
                # Use the first available model
                self.config.set("ai.model", models[0])
                self.config.set("ai.enabled", True)
                self.config.save()
                return True

        # Disable AI if not available
        self.config.set("ai.enabled", False)
        self.config.save()
        return False

    def quick_setup(self):
        """Run a quick, non-interactive setup"""
        self.detect_and_configure_ai()

        # Set reasonable defaults
        self.config.set("terminal.history_size", 1000)
        self.config.set("ai.help_on_error", True)
        self.config.save()

        # Mark setup as completed
        marker_file = Path.home() / ".termsage" / ".setup_completed"
        marker_file.parent.mkdir(parents=True, exist_ok=True)
        marker_file.touch()


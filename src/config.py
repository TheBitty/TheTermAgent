"""
Configuration Management - Load and save user preferences
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from decorators import PathManager

    c_CONFIG_FILE = PathManager.get_config_file()
except ImportError:
    # Fallback if decorators not available
    c_CONFIG_DIR = Path.home() / ".termsage"
    c_CONFIG_FILE = c_CONFIG_DIR / "config.json"

# Default configuration
c_DEFAULT_CONFIG = {
    "terminal": {"history_size": 1000, "prompt_style": "simple", "start_with_sudo": False},
    "ai": {"model": "llama2", "enabled": True, "help_on_error": True, "base_url": "http://localhost:11434"},
}


class Config:
    """Manages user configuration and preferences"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration

        Args:
            config_path: Optional custom config file path
        """
        self.config_path = Path(config_path) if config_path else c_CONFIG_FILE
        self.settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create with defaults

        Returns:
            Configuration dictionary
        """
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing config or use defaults
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)

                # Merge with defaults to ensure all keys exist
                merged_config = self._merge_configs(c_DEFAULT_CONFIG, config)

                # Save back if we added new default keys
                if merged_config != config:
                    self._save_config(merged_config)

                return merged_config

            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file ({e}). Using defaults.")
                # Save defaults and use them
                self._save_config(c_DEFAULT_CONFIG)
                return c_DEFAULT_CONFIG.copy()
        else:
            # First run - create config with defaults
            print(f"Creating config file at {self.config_path}")
            self._save_config(c_DEFAULT_CONFIG)
            return c_DEFAULT_CONFIG.copy()

    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """
        Recursively merge user config with defaults

        Args:
            default: Default configuration
            user: User configuration

        Returns:
            Merged configuration
        """
        result = default.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to file

        Args:
            config: Configuration to save
        """
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation

        Args:
            key: Configuration key (e.g., "ai.model")
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.settings

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation

        Args:
            key: Configuration key (e.g., "ai.model")
            value: Value to set
        """
        keys = key.split(".")
        target = self.settings

        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]

        # Set the value
        target[keys[-1]] = value

    def save(self) -> None:
        """Save current configuration to file"""
        self._save_config(self.settings)

    def get_ai_config(self) -> Dict[str, Any]:
        """
        Get all AI-related configuration

        Returns:
            AI configuration dictionary
        """
        return self.settings.get("ai", {})

    def get_terminal_config(self) -> Dict[str, Any]:
        """
        Get all terminal-related configuration

        Returns:
            Terminal configuration dictionary
        """
        return self.settings.get("terminal", {})

    def is_ai_enabled(self) -> bool:
        """Check if AI features are enabled"""
        return self.get("ai.enabled", True)

    def get_ollama_model(self) -> str:
        """Get the current Ollama model"""
        return self.get("ai.model", "llama2")

    def set_ollama_model(self, model: str) -> None:
        """Set the Ollama model and save config"""
        self.set("ai.model", model)
        self.save()
        print(f"Model set to: {model}")

    def get_ollama_url(self) -> str:
        """Get the Ollama base URL"""
        return self.get("ai.base_url", "http://localhost:11434")

    def is_sudo_enabled(self) -> bool:
        """Check if sudo mode is enabled for startup"""
        return self.get("terminal.start_with_sudo", False)

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults"""
        self.settings = c_DEFAULT_CONFIG.copy()
        self.save()
        print("Configuration reset to defaults")

    def show_config(self) -> None:
        """Display current configuration"""
        print("Current Configuration:")
        print(json.dumps(self.settings, indent=2))


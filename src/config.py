import os
import json
from typing import Dict, Any

# Default Ollama settings
c_DEFAULT_OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "default_model": "llama2",
    "timeout": 30,
    "max_retries": 3
}

class Config:
    def __init__(self, user_config_path: str = "config.user.json"):
        self.user_config_path = user_config_path
        self.settings = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with user overrides"""
        # Start with defaults
        config = c_DEFAULT_OLLAMA_CONFIG.copy()
        
        # Apply user overrides if file exists
        if os.path.exists(self.user_config_path):
            try:
                with open(self.user_config_path, 'r') as f:
                    user_settings = json.load(f)
                    # Simple update - user settings override defaults
                    config.update(user_settings)
            except (json.JSONDecodeError, IOError):
                # If there's an error, just use defaults
                pass
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get all Ollama-related settings"""
        return self.settings.copy()

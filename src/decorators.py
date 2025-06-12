"""
Decorators and utilities for TermSage
"""

import functools
import requests
from typing import Callable, Any
from ui_utils import UIUtils

class AIUnavailableError(Exception):
    """Raised when AI functionality is required but unavailable"""
    pass

def requires_ai(ui: UIUtils = None):
    """Decorator to handle AI availability checks"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'ollama') and not self.ollama.is_available():
                error_msg = "AI not available. Make sure Ollama is running with: ollama serve"
                if ui:
                    print(ui.warning(error_msg))
                else:
                    print(f"⚠️  {error_msg}")
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def handle_requests_errors(operation_name: str = "operation", ui: UIUtils = None):
    """Decorator to handle common request errors consistently"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.Timeout:
                error_msg = f"⏱️ Timeout during {operation_name}. Try again or use a faster model."
                if ui:
                    print(ui.error(error_msg))
                else:
                    print(error_msg)
                return None
            except requests.ConnectionError:
                error_msg = f"❌ Connection failed during {operation_name}. Check your network."
                if ui:
                    print(ui.error(error_msg))
                else:
                    print(error_msg)
                return None
            except requests.RequestException as e:
                error_msg = f"❌ Request error during {operation_name}: {e}"
                if ui:
                    print(ui.error(error_msg))
                else:
                    print(error_msg)
                return None
            except Exception as e:
                error_msg = f"❌ Unexpected error during {operation_name}: {e}"
                if ui:
                    print(ui.error(error_msg))
                else:
                    print(error_msg)
                return None
        return wrapper
    return decorator

class PathManager:
    """Centralized path management for TermSage"""
    
    from pathlib import Path
    
    BASE_DIR = Path.home() / ".termsage"
    
    @classmethod
    def ensure_base_dir(cls):
        """Ensure the base directory exists"""
        cls.BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_config_file(cls) -> Path:
        """Get the config file path"""
        cls.ensure_base_dir()
        return cls.BASE_DIR / "config.json"
    
    @classmethod
    def get_history_file(cls) -> Path:
        """Get the history file path"""
        cls.ensure_base_dir()
        return cls.BASE_DIR / "history"
    
    @classmethod
    def get_marker_file(cls, name: str) -> Path:
        """Get a marker file path"""
        cls.ensure_base_dir()
        return cls.BASE_DIR / f".{name}_completed"
    
    @classmethod
    def get_cache_file(cls, name: str) -> Path:
        """Get a cache file path"""
        cls.ensure_base_dir()
        return cls.BASE_DIR / "cache" / f"{name}.json"

def with_loading_indicator(message: str = "Processing", ui: UIUtils = None):
    """Decorator to show loading indicator during function execution"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if ui:
                from ui_utils import LoadingIndicator
                indicator = LoadingIndicator(message, ui)
                indicator.start()
                try:
                    result = func(*args, **kwargs)
                    indicator.stop()
                    return result
                except Exception as e:
                    indicator.stop()
                    raise e
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
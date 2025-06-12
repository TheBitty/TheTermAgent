"""
Ollama Integration - Interface with local Ollama installation
"""

import requests
import json
import os
from typing import List, Dict, Optional
from decorators import handle_requests_errors

class OllamaHelper:
    """Handles communication with local Ollama instance"""
    
    def __init__(self, config):
        """
        Initialize Ollama helper
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.base_url = config.get_ollama_url()
        self.current_model = config.get_ollama_model()
    
    def _make_request(self, endpoint: str, method: str = "GET", 
                     json_data: dict = None, timeout: int = 10) -> requests.Response:
        """
        Base method for all Ollama API requests
        
        Args:
            endpoint: API endpoint (without /api/ prefix)
            method: HTTP method
            json_data: JSON data for POST requests
            timeout: Request timeout in seconds
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: For any request errors
        """
        response = requests.request(
            method, 
            f"{self.base_url}/api/{endpoint}",
            json=json_data, 
            timeout=timeout
        )
        response.raise_for_status()
        return response

    def is_available(self) -> bool:
        """
        Check if Ollama is running and accessible
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            self._make_request("tags", timeout=5)
            return True
        except:
            return False
    
    def list_models(self) -> None:
        """List all installed Ollama models"""
        if not self.is_available():
            print("❌ Error: Cannot connect to Ollama.")
            print("   Make sure Ollama is running: ollama serve")
            return
        
        try:
            response = self._make_request("tags", timeout=10)
            data = response.json()
            models = data.get("models", [])
            
            if not models:
                print("No Ollama models installed.")
                print("Install a model with: ollama pull llama2")
                return
            
            print("\\n📋 Installed Ollama models:")
            for model in models:
                name = model["name"]
                size_gb = model.get("size", 0) / (1024**3)  # Convert to GB
                
                if name == self.current_model:
                    print(f"  ✓ {name} ({size_gb:.1f}GB) (current)")
                else:
                    print(f"    {name} ({size_gb:.1f}GB)")
            
            print(f"\\nCurrent model: {self.current_model}")
            print("Switch with: /model <model_name>")
            
        except requests.RequestException as e:
            print(f"❌ Error connecting to Ollama: {e}")
        except Exception as e:
            print(f"❌ Error listing models: {e}")
    
    def switch_model(self, model_name: str) -> bool:
        """
        Switch to a different Ollama model
        
        Args:
            model_name: Name of the model to switch to
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            print("❌ Error: Cannot connect to Ollama")
            return False
        
        try:
            # Get available models
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            models = [m["name"] for m in response.json().get("models", [])]
            
            # Check if model exists
            if model_name not in models:
                print(f"❌ Model '{model_name}' not found.")
                print("Available models:")
                for model in models:
                    print(f"  - {model}")
                print(f"\\nInstall with: ollama pull {model_name}")
                return False
            
            # Switch model
            self.current_model = model_name
            self.config.set_ollama_model(model_name)
            print(f"✓ Switched to model: {model_name}")
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error connecting to Ollama: {e}")
            return False
        except Exception as e:
            print(f"❌ Error switching model: {e}")
            return False
    
    def get_help(self, command: str) -> str:
        """
        Get AI help for a command with context awareness
        
        Args:
            command: Command to get help for
            
        Returns:
            AI-generated help text
        """
        if not command.strip():
            return "Please specify a command to get help for."
        
        if not self.is_available():
            return ("❌ Ollama not available. Make sure it's running:\\n"
                   "   ollama serve")
        
        # Check cache first for performance
        cache_key = f"help_{command}_{os.getcwd()}"
        if hasattr(self, '_help_cache') and cache_key in self._help_cache:
            return self._help_cache[cache_key]
        
        # Detect context
        context = self._detect_context()
        
        # Create smart, context-aware prompt
        prompt = self._create_smart_prompt(command, context)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Lower temperature for more focused responses
                        "num_predict": 150   # Reduced from 300 for performance
                    }
                },
                timeout=15  # Reduced timeout for faster responses
            )
            
            response.raise_for_status()
            result = response.json()
            
            ai_response = result.get("response", "").strip()
            
            if ai_response:
                # Initialize cache if needed
                if not hasattr(self, '_help_cache'):
                    self._help_cache = {}
                
                # Cache the response
                formatted_response = f"💡 {ai_response}"
                self._help_cache[cache_key] = formatted_response
                
                # Keep cache size manageable
                if len(self._help_cache) > 20:
                    self._help_cache.pop(next(iter(self._help_cache)))
                
                return formatted_response
            else:
                return "❌ No response from AI model"
                
        except requests.Timeout:
            return f"⏱️ Response timeout. Try: man {command}"
        except requests.RequestException as e:
            return f"❌ Connection error. Try: man {command}"
        except Exception as e:
            return f"❌ Error getting help: {e}"
    
    def _detect_context(self) -> dict:
        """Detect current directory context for smarter help"""
        context = {
            'is_git_repo': os.path.exists('.git'),
            'is_node_project': os.path.exists('package.json'),
            'is_python_project': os.path.exists('requirements.txt') or os.path.exists('pyproject.toml'),
            'is_docker_project': os.path.exists('Dockerfile'),
            'current_dir': os.path.basename(os.getcwd()) if os.getcwd() != '/' else 'root'
        }
        return context
    
    def is_help_cached(self, command: str) -> bool:
        """Check if help for command is cached"""
        cache_key = f"help_{command}_{os.getcwd()}"
        return hasattr(self, '_help_cache') and cache_key in self._help_cache
    
    def _create_smart_prompt(self, command: str, context: dict) -> str:
        """Create context-aware, concise prompt"""
        base_cmd = command.split()[0] if ' ' in command else command
        
        # Context-specific prompts for common commands
        if base_cmd == 'git' and context['is_git_repo']:
            return f"""Quick git help for: {command}

Context: In git repository
Give 2-3 most useful examples for this git command. Focus on practical usage, not explanations."""
        
        elif base_cmd == 'npm' and context['is_node_project']:
            return f"""Quick npm help for: {command}

Context: Node.js project
Give 2-3 most useful examples. Focus on practical commands for this project."""
        
        elif base_cmd == 'docker' and context['is_docker_project']:
            return f"""Quick docker help for: {command}

Context: Docker project detected
Give 2-3 most useful examples for working with this project."""
        
        elif base_cmd in ['pip', 'python'] and context['is_python_project']:
            return f"""Quick Python help for: {command}

Context: Python project
Give 2-3 most useful examples for this project."""
        
        # Default concise prompt for other commands
        return f"""Quick help for: {command}

Give 2-3 most useful examples. Skip explanations, focus on practical syntax."""
    
    def test_model(self) -> bool:
        """
        Test if current model is working
        
        Returns:
            True if model responds, False otherwise
        """
        if not self.is_available():
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": "Say 'Hello' if you can understand this.",
                    "stream": False,
                    "options": {"num_predict": 10}
                },
                timeout=15
            )
            
            response.raise_for_status()
            result = response.json()
            return "hello" in result.get("response", "").lower()
            
        except:
            return False
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        if not self.is_available():
            return {}
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            for model in models:
                if model["name"] == self.current_model:
                    return model
            
            return {}
            
        except:
            return {}
    
    def chat(self, message: str) -> str:
        """
        Have a chat conversation with the AI
        
        Args:
            message: User's message
            
        Returns:
            AI response
        """
        if not message.strip():
            return "Please provide a message to chat about."
        
        if not self.is_available():
            return "❌ Ollama not available. Make sure it's running with: ollama serve"
        
        # Create chat prompt
        prompt = f"""You are a helpful terminal assistant. The user is asking: {message}

Provide a helpful, practical response. If it's about terminal commands, include examples.
Be concise but thorough."""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500
                    }
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            ai_response = result.get("response", "").strip()
            return ai_response if ai_response else "❌ No response from AI model"
                
        except requests.Timeout:
            return f"⏱️ Timeout waiting for {self.current_model}. Try a smaller model."
        except requests.RequestException as e:
            return f"❌ Error connecting to Ollama: {e}"
        except Exception as e:
            return f"❌ Error in chat: {e}"
    
    def get_error_help(self, command: str, error_output: str) -> str:
        """
        Get AI help for command errors
        
        Args:
            command: The command that failed
            error_output: Error message from the command
            
        Returns:
            AI suggestions for fixing the error
        """
        if not self.is_available():
            return "❌ Ollama not available for error analysis"
        
        prompt = f"""You are a helpful terminal assistant. A command failed with an error:

Command: {command}
Error: {error_output}

Provide specific suggestions to fix this error. Include:
1. Most likely cause
2. Specific commands to try
3. Alternative approaches if needed

Be concise and practical."""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 200
                    }
                },
                timeout=20
            )
            
            response.raise_for_status()
            result = response.json()
            
            ai_response = result.get("response", "").strip()
            return ai_response if ai_response else "❌ No suggestions available"
                
        except:
            return "❌ Error getting AI suggestions"
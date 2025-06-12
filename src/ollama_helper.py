"""
Ollama Integration - Interface with local Ollama installation
"""

import requests
import json
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
        Get AI help for a command
        
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
        
        # Create help prompt
        prompt = f"""You are a helpful terminal assistant. Explain this command concisely:

Command: {command}

Provide:
1. What the command does
2. Common usage examples  
3. Important flags/options
4. Any safety warnings if needed

Keep it practical and brief."""
        
        try:
            print(f"🤔 Getting help for '{command}' from {self.current_model}...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300  # Limit response length
                    }
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            ai_response = result.get("response", "").strip()
            
            if ai_response:
                return f"🤖 {self.current_model}:\\n{ai_response}"
            else:
                return "❌ No response from AI model"
                
        except requests.Timeout:
            return f"⏱️ Timeout waiting for {self.current_model}. Try a smaller model."
        except requests.RequestException as e:
            return f"❌ Error connecting to Ollama: {e}"
        except Exception as e:
            return f"❌ Error getting help: {e}"
    
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
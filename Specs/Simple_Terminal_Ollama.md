# Feature Specification: Simple Terminal with Ollama Integration

## Feature Name:
Basic Terminal with Ollama AI Help

## Problem Statement:
Users need a working terminal that can execute commands normally, with optional AI help using any Ollama model they have installed locally. The solution should be simple, privacy-focused, and work offline.

## Proposed Solution:
1. Build a functional terminal that executes system commands
2. Add Ollama integration for command help (using `?` suffix)
3. Let users choose any installed Ollama model
4. Save user preferences in a config file

## Requirements:

### Functional Requirements:
1. **Terminal Basics**
   - Execute any system command
   - Show output (stdout/stderr)
   - Support cd, exit, clear
   - Command history with arrow keys
   - Show current directory in prompt

2. **Ollama Integration**
   - `command?` asks Ollama for help
   - List available Ollama models
   - Let user switch models with `/model`
   - Work with any model the user has installed
   - Show model being used

3. **Configuration**
   - Save user's preferred Ollama model
   - Remember terminal preferences
   - Store in `~/.termsage/config.json`
   - Auto-create config on first run

### Non-functional Requirements:
1. **Simplicity**: Minimal dependencies, clean code
2. **Performance**: Fast command execution, async AI calls
3. **Reliability**: Works without AI, graceful Ollama failures
4. **Privacy**: Everything stays local

## Acceptance Criteria:
- [ ] Terminal executes commands like bash/zsh
- [ ] `git?` returns help from Ollama
- [ ] `/models` lists installed Ollama models
- [ ] `/model llama2` switches to that model
- [ ] Config saves user's model choice
- [ ] Works offline with local Ollama

## Technical Design Notes:

### Simple Architecture:
```
main.py
  ├── Terminal loop (get input, execute)
  ├── CommandHandler (execute commands)
  └── OllamaHelper (AI assistance)
       └── Config (load/save preferences)
```

### Key Components:

1. **Main Terminal Loop** (`main.py`)
```python
import readline
from command_handler import CommandHandler
from ollama_helper import OllamaHelper
from config import Config

def main():
    config = Config()
    command_handler = CommandHandler()
    ollama = OllamaHelper(config)
    
    # Setup readline for history
    readline.parse_and_bind("tab: complete")
    
    while True:
        try:
            # Show prompt with current directory
            prompt = f"{os.getcwd()} $ "
            user_input = input(prompt)
            
            # Check for special commands
            if user_input == "exit":
                break
            elif user_input == "/models":
                ollama.list_models()
                continue
            elif user_input.startswith("/model "):
                model_name = user_input[7:]
                ollama.switch_model(model_name)
                config.save()
                continue
            elif user_input.endswith("?"):
                # Get AI help
                command = user_input[:-1]
                help_text = ollama.get_help(command)
                print(help_text)
                continue
            
            # Execute normal command
            command_handler.execute(user_input)
            
        except KeyboardInterrupt:
            print("\n^C")
            continue
        except EOFError:
            break
```

2. **Ollama Helper** (`ollama_helper.py`)
```python
import requests
import json

class OllamaHelper:
    def __init__(self, config):
        self.config = config
        self.base_url = "http://localhost:11434"
        self.current_model = config.get("ai.model", "llama2")
    
    def list_models(self):
        """List all installed Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json()["models"]
            print("\nInstalled Ollama models:")
            for model in models:
                name = model["name"]
                if name == self.current_model:
                    print(f"  * {name} (current)")
                else:
                    print(f"    {name}")
        except:
            print("Error: Cannot connect to Ollama. Is it running?")
    
    def switch_model(self, model_name):
        """Switch to a different Ollama model"""
        # Check if model exists
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = [m["name"] for m in response.json()["models"]]
            
            if model_name in models:
                self.current_model = model_name
                self.config.set("ai.model", model_name)
                print(f"Switched to model: {model_name}")
            else:
                print(f"Model '{model_name}' not found. Use /models to see available models.")
        except:
            print("Error: Cannot connect to Ollama")
    
    def get_help(self, command):
        """Get help for a command from Ollama"""
        prompt = f"""You are a helpful terminal assistant. 
        Explain this command concisely with practical examples: {command}
        Keep it brief and focus on common usage."""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()["response"]
        except:
            return f"Error: Cannot get help. Is Ollama running with {self.current_model}?"
```

3. **Enhanced Config** (`config.py`)
```python
import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".termsage"
        self.config_file = self.config_dir / "config.json"
        self.settings = self._load_config()
    
    def _load_config(self):
        """Load or create config"""
        # Create directory if needed
        self.config_dir.mkdir(exist_ok=True)
        
        # Default settings
        defaults = {
            "terminal": {
                "history_size": 1000,
                "prompt_style": "simple"
            },
            "ai": {
                "model": "llama2",
                "enabled": True,
                "help_on_error": True
            }
        }
        
        # Load existing or use defaults
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return defaults
        else:
            # Save defaults on first run
            self.settings = defaults
            self.save()
            return defaults
    
    def get(self, key, default=None):
        """Get nested config value using dot notation"""
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        """Set nested config value"""
        keys = key.split('.')
        target = self.settings
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
    
    def save(self):
        """Save config to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
```

### Command Handler stays simple:
```python
import subprocess
import os

class CommandHandler:
    def execute(self, command):
        """Execute a system command"""
        # Handle cd specially
        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                os.chdir(os.path.expanduser(path))
            except Exception as e:
                print(f"cd: {e}")
            return
        
        # Execute other commands
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Print output
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='')
                
        except Exception as e:
            print(f"Error: {e}")
```

## Implementation Order:
1. Get basic terminal working (execute commands, show output)
2. Add Ollama model listing (`/models`)
3. Add command help (`command?`)
4. Add model switching (`/model name`)
5. Save preferences to config
6. Add command history

## Testing Checklist:
- [ ] Run basic commands: ls, pwd, echo
- [ ] Test cd changes directory
- [ ] Test /models shows Ollama models
- [ ] Test git? returns help
- [ ] Test /model llama2 switches model
- [ ] Verify config saves model choice
- [ ] Test without Ollama running (graceful failure)

## Configuration Example:
```json
{
  "terminal": {
    "history_size": 1000,
    "prompt_style": "simple"
  },
  "ai": {
    "model": "mistral",
    "enabled": true,
    "help_on_error": true
  }
}
```

## Future Enhancements (after MVP):
- Streaming responses for long AI output
- Auto-help when commands fail
- Tab completion
- Syntax highlighting
- Multiple AI providers
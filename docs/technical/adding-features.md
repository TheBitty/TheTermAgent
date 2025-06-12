# Adding Features to TermSage

## Overview
This guide provides step-by-step instructions for adding new features to TermSage. It covers the development process, code patterns, integration points, and best practices for extending the system while maintaining compatibility and code quality.

## Feature Development Process

### 1. Planning and Design

**Before writing code, consider:**
- **Feature scope**: What exactly will this feature do?
- **User interface**: How will users interact with this feature?
- **Component impact**: Which existing components will be affected?
- **Configuration needs**: What settings might users want to customize?
- **AI integration**: Will this feature benefit from AI assistance?
- **Performance impact**: How will this affect system performance?

**Design Questions to Answer:**
```
□ Is this a new command, UI enhancement, or system improvement?
□ Does it require new configuration options?
□ Will it need state management across commands?
□ Does it interact with external services?
□ How should errors be handled?
□ What are the testing requirements?
```

### 2. Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-feature-name

# 2. Set up development environment
source venv/bin/activate
pip install -r requirements.txt

# 3. Make sure Ollama is running for AI features
ollama serve

# 4. Run TermSage to understand current behavior
python src/main.py

# 5. Implement feature (following this guide)

# 6. Test thoroughly
python -m pytest tests/
python src/main.py  # Manual testing

# 7. Update documentation

# 8. Commit and create pull request
git add .
git commit -m "feat: add new feature description"
```

## Feature Categories and Implementation Patterns

### Category 1: New Built-in Commands

**Example**: Adding a `/status` command to show system status

**Step 1: Register the Command**
```python
# In src/command_registry.py, modify CommandRegistry.__init__()
def __init__(self, ui: UIUtils, help_system, onboarding, ollama, config):
    # ... existing code ...
    
    # Add new command to the registry
    self.commands: Dict[str, Callable] = {
        "exit": self.handle_exit,
        "help": self.handle_help,
        "/tutorial": self.handle_tutorial,
        "/setup": self.handle_setup,
        "/chat": self.handle_chat,
        "clear": self.handle_clear,
        "/models": self.handle_models,
        "/config": self.handle_config,
        "/status": self.handle_status,  # ← New command
    }
```

**Step 2: Implement the Handler**
```python
# In src/command_registry.py, add new method
def handle_status(self) -> bool:
    """Handle status command - show system information"""
    print(self.ui.info("TermSage System Status"))
    print("─" * 30)
    
    # AI status
    if self.ollama.is_available():
        model_info = self.ollama.get_model_info()
        print(f"AI: {self.ui.success('Available')} (Model: {self.ollama.current_model})")
    else:
        print(f"AI: {self.ui.warning('Unavailable')}")
    
    # Configuration status
    config_path = self.config.config_path
    print(f"Config: {self.ui.success(str(config_path))}")
    
    # State information
    if self.state:
        print(f"Commands executed: {self.state.command_count}")
        print(f"Mode: {'Chat' if self.state.chat_mode else 'Normal'}")
    
    # System information
    import sys
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")
    
    return True
```

**Step 3: Add Help Documentation**
```python
# In src/ui_utils.py, update show_help() function
def show_help():
    """Display comprehensive help information"""
    ui = UIUtils()
    help_text = f"""
{ui.colorize('TermSage Help', Color.BRIGHT_WHITE, bold=True)}
{ui.colorize('═' * 50, Color.BRIGHT_CYAN)}

{ui.colorize('🚀 QUICK START', Color.BRIGHT_YELLOW, bold=True)}
  {ui.command('help')}              Show this help message
  {ui.command('/tutorial')}         Interactive feature walkthrough
  {ui.command('/status')}           Show system status information  ← New
  {ui.command('command?')}          Get AI help for any command
  {ui.command('/chat')}             Start conversational AI mode
  {ui.command('exit')}              Exit TermSage
  
  # ... rest of help text ...
```

**Step 4: Test the Feature**
```bash
# Manual testing
python src/main.py
$ /status
# Should display system status information

# Add unit test
# tests/test_command_registry.py
def test_handle_status(self):
    # Test implementation
    pass
```

### Category 2: Enhanced AI Features

**Example**: Adding a `/explain` command that explains the last command

**Step 1: Extend AppState to Track Last Command**
```python
# In src/command_registry.py, modify AppState class
class AppState:
    def __init__(self):
        self.chat_mode = False
        self.recent_commands = []
        self.command_count = 0
        self.last_command = None        # ← New field
        self.last_command_result = None # ← New field
    
    def set_last_command(self, command: str, result: CommandResult = None):
        """Track the last executed command and its result"""
        self.last_command = command
        self.last_command_result = result
```

**Step 2: Update Main Loop to Track Commands**
```python
# In src/main.py, modify the main loop
def main():
    # ... initialization ...
    
    while True:
        try:
            # ... existing code ...
            
            # Execute normal command with enhanced error handling
            try:
                cmd_result = command_handler.execute(user_input)
                
                # Track the command and result  ← New
                state.set_last_command(user_input, cmd_result)
                
                # ... rest of error handling ...
```

**Step 3: Add OllamaHelper Method**
```python
# In src/ollama_helper.py, add new method
def explain_command(self, command: str, result: CommandResult = None) -> str:
    """
    Explain what a command does and analyze its results
    
    Args:
        command: The command that was executed
        result: The result of command execution (optional)
        
    Returns:
        AI explanation of the command
    """
    if not command.strip():
        return "No command to explain."
    
    if not self.is_available():
        return ("❌ Ollama not available. Try: man " + command.split()[0])
    
    # Detect context for better explanations
    context = self._detect_context()
    
    # Create explanation prompt
    prompt = self._create_explanation_prompt(command, result, context)
    
    try:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.current_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 200
                }
            },
            timeout=20
        )
        
        response.raise_for_status()
        result = response.json()
        
        ai_response = result.get("response", "").strip()
        return ai_response if ai_response else "❌ No explanation available"
        
    except requests.Timeout:
        return f"⏱️ Explanation timeout. Try: man {command.split()[0]}"
    except requests.RequestException as e:
        return f"❌ Error getting explanation: {e}"

def _create_explanation_prompt(self, command: str, result: CommandResult, context: dict) -> str:
    """Create a specialized prompt for command explanation"""
    base_cmd = command.split()[0] if ' ' in command else command
    
    prompt = f"""Explain this command in simple terms: {command}

What it does:
- Purpose and function
- Key arguments/options used
- Expected behavior

Context: {context.get('current_dir', 'unknown directory')}"""
    
    # Add result analysis if available
    if result and result.exit_code == 0:
        prompt += f"\n\nCommand succeeded and produced output."
    elif result and result.exit_code != 0:
        prompt += f"\n\nCommand failed with exit code {result.exit_code}."
    
    prompt += "\n\nProvide a concise, beginner-friendly explanation."
    
    return prompt
```

**Step 4: Add Command Handler**
```python
# In src/command_registry.py
def handle_explain(self) -> bool:
    """Handle explain command - explain the last command"""
    if not self.state or not self.state.last_command:
        print(self.ui.warning("No recent command to explain"))
        return True
    
    command = self.state.last_command
    result = self.state.last_command_result
    
    print(self.ui.info(f"Explaining: {command}"))
    
    if self.ollama.is_available():
        indicator = LoadingIndicator("Generating explanation", self.ui)
        indicator.start()
        
        try:
            explanation = self.ollama.explain_command(command, result)
            indicator.stop()
            print(self.ui.ai_response(explanation))
        except Exception as e:
            indicator.stop()
            print(self.ui.error(f"Error generating explanation: {e}"))
    else:
        print(self.ui.warning(f"AI not available. Try: man {command.split()[0]}"))
    
    return True

# Don't forget to register it in __init__
self.commands["/explain"] = self.handle_explain
```

### Category 3: UI Enhancements

**Example**: Adding colored syntax highlighting for commands

**Step 1: Extend UIUtils with Syntax Highlighting**
```python
# In src/ui_utils.py
class UIUtils:
    # ... existing methods ...
    
    def highlight_command(self, command: str) -> str:
        """Apply syntax highlighting to command text"""
        if not self.colors_enabled:
            return command
        
        # Split command into parts
        parts = command.split()
        if not parts:
            return command
        
        highlighted_parts = []
        
        # Highlight the base command
        base_cmd = parts[0]
        if base_cmd in self._get_common_commands():
            highlighted_parts.append(self.colorize(base_cmd, Color.BRIGHT_BLUE, bold=True))
        else:
            highlighted_parts.append(base_cmd)
        
        # Highlight flags and arguments
        for part in parts[1:]:
            if part.startswith('-'):
                # Command flags
                highlighted_parts.append(self.colorize(part, Color.BRIGHT_YELLOW))
            elif '=' in part:
                # Key=value pairs
                key, value = part.split('=', 1)
                highlighted = f"{self.colorize(key, Color.BRIGHT_CYAN)}={self.colorize(value, Color.BRIGHT_GREEN)}"
                highlighted_parts.append(highlighted)
            else:
                # Regular arguments
                highlighted_parts.append(self.colorize(part, Color.WHITE))
        
        return ' '.join(highlighted_parts)
    
    def _get_common_commands(self) -> set:
        """Return set of common commands for highlighting"""
        return {
            'ls', 'cd', 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'grep', 'find',
            'git', 'docker', 'npm', 'pip', 'python', 'node', 'vim', 'nano',
            'tar', 'curl', 'wget', 'ssh', 'scp', 'systemctl', 'ps', 'top'
        }
```

**Step 2: Integrate with Help System**
```python
# In src/help_system.py, modify tutorial methods
def _tutorial_basic_commands(self) -> bool:
    """Tutorial step 2: Basic enhanced commands"""
    print(f"{self.ui.colorize('🔧 Enhanced Commands', self.ui.Color.BRIGHT_BLUE, bold=True)}")
    print("TermSage works like any terminal, but with AI superpowers.\n")
    
    # Use syntax highlighting for examples
    example_cmd = "ls -la --color=auto"
    highlighted = self.ui.highlight_command(example_cmd)
    print(f"{self.ui.info('Try this:')} {highlighted}")
    
    return True
```

### Category 4: Configuration Extensions

**Example**: Adding auto-save configuration for command history

**Step 1: Extend Default Configuration**
```python
# In src/config.py, modify c_DEFAULT_CONFIG
c_DEFAULT_CONFIG = {
    "terminal": {
        "history_size": 1000,
        "prompt_style": "simple",
        "auto_save_history": True,      # ← New option
        "history_save_interval": 10     # ← New option (commands)
    },
    "ai": {
        "model": "llama2",
        "enabled": True,
        "help_on_error": True,
        "base_url": "http://localhost:11434"
    }
}
```

**Step 2: Add Configuration Accessors**
```python
# In src/config.py, add new methods
def is_auto_save_history_enabled(self) -> bool:
    """Check if auto-save history is enabled"""
    return self.get('terminal.auto_save_history', True)

def get_history_save_interval(self) -> int:
    """Get history save interval in commands"""
    return self.get('terminal.history_save_interval', 10)
```

**Step 3: Implement Auto-Save Logic**
```python
# In src/main.py, modify main() function
def main():
    # ... initialization ...
    
    commands_since_save = 0  # Track commands for auto-save
    
    while True:
        try:
            # ... existing code ...
            
            # Track command for contextual help
            state.add_command(user_input)
            commands_since_save += 1
            
            # Auto-save history if enabled
            if (config.is_auto_save_history_enabled() and 
                commands_since_save >= config.get_history_save_interval()):
                save_history()
                commands_since_save = 0
            
            # ... rest of loop ...
```

### Category 5: AI Provider Extensions

**Example**: Adding support for different AI models per task type

**Step 1: Extend Configuration for Task-Specific Models**
```python
# In src/config.py, extend default config
c_DEFAULT_CONFIG = {
    # ... existing config ...
    "ai": {
        "model": "llama2",
        "enabled": True,
        "help_on_error": True,
        "base_url": "http://localhost:11434",
        "task_models": {                    # ← New section
            "help": "llama2",
            "chat": "llama2", 
            "code": "codellama",
            "explain": "llama2:13b"
        }
    }
}
```

**Step 2: Extend OllamaHelper for Task-Specific Models**
```python
# In src/ollama_helper.py, add model selection logic
def get_model_for_task(self, task_type: str) -> str:
    """Get the appropriate model for a specific task type"""
    task_models = self.config.get('ai.task_models', {})
    return task_models.get(task_type, self.current_model)

def get_help(self, command: str) -> str:
    """Get AI help using task-specific model"""
    # ... existing code ...
    
    # Use task-specific model
    model_for_help = self.get_model_for_task('help')
    
    try:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model_for_help,  # ← Use task-specific model
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 150
                }
            },
            timeout=15
        )
        # ... rest of implementation ...
```

## Testing New Features

### Unit Testing Patterns

**Test Structure**:
```python
# tests/test_new_feature.py
import pytest
from unittest.mock import Mock, patch
from src.command_registry import CommandRegistry
from src.ui_utils import UIUtils
from src.config import Config

class TestNewFeature:
    def setup_method(self):
        """Setup test fixtures"""
        self.config = Config()
        self.ui = UIUtils()
        self.ollama = Mock()
        self.help_system = Mock()
        self.onboarding = Mock()
        
        self.registry = CommandRegistry(
            self.ui, self.help_system, self.onboarding, 
            self.ollama, self.config
        )
    
    def test_new_command_success(self):
        """Test successful execution of new command"""
        result = self.registry.handle_status()
        assert result is True
        # Add specific assertions
    
    def test_new_command_failure(self):
        """Test error handling in new command"""
        self.ollama.is_available.return_value = False
        result = self.registry.handle_status()
        assert result is True  # Should not crash
    
    @patch('requests.post')
    def test_ai_integration(self, mock_post):
        """Test AI integration for new feature"""
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Test explanation"}
        mock_post.return_value = mock_response
        
        result = self.ollama.explain_command("ls -la")
        assert "Test explanation" in result
```

### Integration Testing

**Manual Testing Checklist**:
```bash
# 1. Basic functionality
python src/main.py
$ /new-command
# Verify expected behavior

# 2. Error conditions
# Stop Ollama service
sudo systemctl stop ollama
$ /new-command
# Verify graceful degradation

# 3. Configuration interaction
# Modify ~/.termsage/config.json
$ /new-command
# Verify configuration is respected

# 4. State interaction
$ /chat
> test chat
$ /exit
$ /new-command
# Verify state changes are handled

# 5. UI formatting
# Test in different terminals
# Test with colors disabled: TERM=dumb python src/main.py
```

### Performance Testing

**Performance Considerations**:
```python
# Time AI operations
import time

def test_ai_performance():
    start_time = time.time()
    result = ollama.new_ai_feature("test input")
    elapsed = time.time() - start_time
    
    # AI operations should complete within reasonable time
    assert elapsed < 10.0  # 10 second timeout
    assert len(result) > 0  # Should return meaningful content

# Memory usage monitoring
import psutil
import os

def test_memory_usage():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operations
    for i in range(100):
        result = ollama.get_help(f"command_{i}")
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable (less than 50MB)
    assert memory_increase < 50 * 1024 * 1024
```

## Documentation Requirements

### Code Documentation

**Docstring Standards**:
```python
def new_feature_method(self, param1: str, param2: int = 10) -> str:
    """
    Brief description of what this method does.
    
    This method performs X operation by doing Y. It integrates with
    the AI system to provide Z functionality.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default value
        
    Returns:
        Description of return value
        
    Raises:
        RequestException: When AI service is unavailable
        ValueError: When parameters are invalid
        
    Example:
        >>> result = obj.new_feature_method("test", 5)
        >>> print(result)
        'Expected output format'
    """
    pass
```

### User Documentation Updates

**Update Required Files**:
1. **AI Docs/User_Guide.md**: Add user-facing feature description
2. **AI Docs/Configuration_Guide.md**: Document any new config options
3. **src/ui_utils.py**: Update help text in `show_help()` function
4. **docs/technical/**: Update relevant technical documentation

**User Documentation Template**:
```markdown
### New Feature Name

**Purpose**: Brief description of what this feature does

**Usage**:
```bash
/new-command [options]
```

**Examples**:
```bash
# Basic usage
$ /new-command
# Expected output...

# With options
$ /new-command --option value
# Expected output...
```

**Configuration**:
```json
{
  "feature": {
    "enabled": true,
    "option": "default_value"
  }
}
```

**Troubleshooting**:
- **Issue**: Feature not working
  - **Solution**: Check configuration and restart TermSage
```

## Best Practices and Guidelines

### Code Quality Standards

**1. Follow Existing Patterns**:
- Use dependency injection for component access
- Follow the existing error handling patterns
- Use UIUtils for all user-facing output
- Access configuration through the Config object

**2. Error Handling**:
```python
# Good: Graceful degradation
def new_feature(self):
    try:
        result = self.ai_operation()
        return self.format_success(result)
    except AIServiceError:
        return self.ui.warning("AI not available, using fallback")
    except Exception as e:
        return self.ui.error(f"Feature failed: {e}")

# Bad: Letting exceptions propagate
def new_feature(self):
    result = self.ai_operation()  # May throw unhandled exception
    return result
```

**3. Configuration Management**:
```python
# Good: Use defaults and validation
setting = self.config.get('feature.setting', 'default_value')
if isinstance(setting, str) and len(setting) > 0:
    # Use setting
else:
    # Use fallback

# Bad: Assume configuration exists
setting = self.config.settings['feature']['setting']  # May KeyError
```

**4. State Management**:
```python
# Good: Check state availability
if self.state:
    self.state.update_feature_data(new_data)

# Bad: Assume state exists
self.state.update_feature_data(new_data)  # May AttributeError
```

### Performance Guidelines

**1. AI Operation Optimization**:
- Use caching for repeated requests
- Implement reasonable timeouts
- Provide loading indicators for long operations
- Use appropriate token limits

**2. Memory Management**:
- Limit cache sizes
- Clean up temporary data
- Avoid storing large objects in state

**3. Startup Performance**:
- Avoid expensive operations during initialization
- Use lazy loading where possible
- Minimize import times

### Security Considerations

**1. Input Validation**:
```python
# Good: Validate user input
def handle_user_input(self, user_input: str):
    if not isinstance(user_input, str):
        return self.ui.error("Invalid input type")
    
    cleaned_input = user_input.strip()
    if len(cleaned_input) == 0:
        return self.ui.warning("Empty input")
    
    # Process validated input
    return self.process_input(cleaned_input)

# Bad: Process input directly
def handle_user_input(self, user_input):
    return self.process_input(user_input)  # No validation
```

**2. File Operations**:
```python
# Good: Safe file handling
def save_feature_data(self, data: dict):
    try:
        file_path = self.config.get_safe_file_path('feature_data.json')
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        return self.ui.error("Permission denied writing feature data")
    except Exception as e:
        return self.ui.error(f"Error saving data: {e}")

# Bad: Unsafe file operations
def save_feature_data(self, data):
    with open('/tmp/feature_data.json', 'w') as f:  # Unsafe path
        json.dump(data, f)  # No error handling
```

## Feature Release Process

### Pre-Release Checklist

```
□ Feature implemented and tested
□ Unit tests written and passing
□ Integration tests completed
□ Documentation updated
□ Performance impact assessed
□ Security review completed
□ Configuration options documented
□ Error handling verified
□ Loading indicators added for slow operations
□ Backward compatibility maintained
```

### Code Review Guidelines

**Review Focus Areas**:
1. **Functionality**: Does the feature work as intended?
2. **Integration**: Does it follow existing patterns?
3. **Error Handling**: Are edge cases covered?
4. **Performance**: Is it efficient and responsive?
5. **Documentation**: Is it properly documented?
6. **Testing**: Are tests comprehensive?

### Deployment Considerations

**Feature Flags** (Future Enhancement):
```python
# Configuration-based feature flags
if self.config.get('features.new_feature_enabled', False):
    return self.handle_new_feature()
else:
    return self.ui.info("Feature not enabled")
```

**Gradual Rollout**:
- Start with experimental flag in configuration
- Gather user feedback
- Enable by default in next release
- Remove flag after feature is stable

This comprehensive guide provides the foundation for successfully adding new features to TermSage while maintaining code quality, performance, and user experience.
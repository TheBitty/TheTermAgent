# Testing and Debugging Guide

## Overview
This guide covers testing strategies, debugging techniques, and quality assurance practices for TermSage development. It provides comprehensive information for testing at all levels, from unit tests to integration testing and performance validation.

## Testing Philosophy

### Testing Pyramid for TermSage
```
                    ┌─────────────────┐
                    │   Manual Tests  │ (UI, Integration, User Acceptance)
                    └─────────────────┘
                ┌───────────────────────────┐
                │   Integration Tests      │ (Component interaction, AI flow)
                └───────────────────────────┘
        ┌─────────────────────────────────────────────┐
        │              Unit Tests                     │ (Individual methods, logic)
        └─────────────────────────────────────────────┘
```

### Testing Principles
1. **Fast Feedback**: Unit tests should run quickly (< 1 second each)
2. **Isolation**: Tests should not depend on external services when possible
3. **Repeatability**: Tests should produce consistent results
4. **Coverage**: Focus on critical paths and edge cases
5. **Maintainability**: Tests should be easy to understand and modify

## Test Environment Setup

### Development Environment
```bash
# 1. Clone repository and setup virtual environment
git clone <repository>
cd TermAgent
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install test dependencies
pip install pytest pytest-cov pytest-mock pytest-asyncio

# 4. Setup Ollama for integration tests
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2:7b  # Lightweight model for testing
ollama serve &

# 5. Create test configuration
mkdir -p ~/.termsage-test
cp config.user.json.example ~/.termsage-test/config.json
```

### Test Configuration
```python
# tests/conftest.py - Pytest configuration
import pytest
import tempfile
import os
from pathlib import Path
from src.config import Config
from src.ui_utils import UIUtils
from src.ollama_helper import OllamaHelper

@pytest.fixture
def temp_config_dir():
    """Create temporary config directory for tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def test_config(temp_config_dir):
    """Create test configuration"""
    config_file = temp_config_dir / "config.json"
    test_config_data = {
        "terminal": {"history_size": 100},
        "ai": {
            "model": "llama2:7b",
            "base_url": "http://localhost:11434",
            "enabled": True
        }
    }
    
    import json
    with open(config_file, 'w') as f:
        json.dump(test_config_data, f)
    
    return Config(str(config_file))

@pytest.fixture
def mock_ollama():
    """Mock Ollama helper for tests that don't need real AI"""
    from unittest.mock import Mock
    ollama = Mock(spec=OllamaHelper)
    ollama.is_available.return_value = True
    ollama.current_model = "llama2:7b"
    ollama.get_help.return_value = "Mocked help response"
    ollama.chat.return_value = "Mocked chat response"
    return ollama

@pytest.fixture
def ui_utils():
    """UIUtils instance for testing"""
    return UIUtils()
```

## Unit Testing

### Testing Command Registry

```python
# tests/test_command_registry.py
import pytest
from unittest.mock import Mock, patch
from src.command_registry import CommandRegistry, AppState

class TestCommandRegistry:
    def setup_method(self):
        """Setup test fixtures"""
        self.ui = Mock()
        self.help_system = Mock()
        self.onboarding = Mock()
        self.ollama = Mock()
        self.config = Mock()
        
        self.registry = CommandRegistry(
            self.ui, self.help_system, self.onboarding,
            self.ollama, self.config
        )
        
        self.state = AppState()
        self.registry.set_state(self.state)
    
    def test_execute_exit_command(self):
        """Test exit command returns False"""
        result = self.registry.execute("exit")
        assert result is False
        self.ui.success.assert_called_with("Goodbye!")
    
    def test_execute_help_command(self):
        """Test help command returns True"""
        with patch('src.command_registry.show_help'):
            result = self.registry.execute("help")
            assert result is True
    
    def test_execute_unknown_command(self):
        """Test unknown command returns None"""
        result = self.registry.execute("unknown_command")
        assert result is None
    
    def test_help_request_with_ai_available(self):
        """Test command help request when AI is available"""
        self.ollama.is_available.return_value = True
        self.ollama.is_help_cached.return_value = False
        self.ollama.get_help.return_value = "Git help response"
        
        result = self.registry.execute("git?")
        
        assert result is True
        self.ollama.get_help.assert_called_with("git")
        self.ui.ai_response.assert_called()
    
    def test_help_request_with_ai_unavailable(self):
        """Test command help request when AI is unavailable"""
        self.ollama.is_available.return_value = False
        
        result = self.registry.execute("git?")
        
        assert result is True
        self.ui.warning.assert_called()
        
    def test_chat_mode_toggle(self):
        """Test chat mode toggling"""
        # Initially not in chat mode
        assert self.state.chat_mode is False
        
        # Toggle to chat mode
        result = self.registry.execute("/chat")
        assert result is True
        assert self.state.chat_mode is True
        
        # Verify UI feedback
        self.ui.info.assert_called()
    
    def test_model_switch_command(self):
        """Test model switching command"""
        self.ollama.is_available.return_value = True
        self.ollama.switch_model.return_value = True
        
        result = self.registry.execute("/model codellama")
        
        assert result is True
        self.ollama.switch_model.assert_called_with("codellama")
    
    def test_model_switch_no_model_name(self):
        """Test model switch without model name"""
        result = self.registry.execute("/model ")
        
        assert result is True
        self.ui.error.assert_called_with("Usage: /model <model_name>")

class TestAppState:
    def setup_method(self):
        self.state = AppState()
    
    def test_initial_state(self):
        """Test initial state values"""
        assert self.state.chat_mode is False
        assert self.state.recent_commands == []
        assert self.state.command_count == 0
    
    def test_add_command(self):
        """Test adding commands to history"""
        self.state.add_command("ls -la")
        self.state.add_command("git status")
        
        assert self.state.command_count == 2
        assert self.state.recent_commands == ["ls -la", "git status"]
    
    def test_command_history_limit(self):
        """Test command history size limit"""
        # Add 55 commands (more than the 50 limit)
        for i in range(55):
            self.state.add_command(f"command_{i}")
        
        # Should only keep last 50
        assert len(self.state.recent_commands) == 50
        assert self.state.recent_commands[0] == "command_5"  # First 5 dropped
        assert self.state.recent_commands[-1] == "command_54"
    
    def test_toggle_chat_mode(self):
        """Test chat mode toggling"""
        # Initially False
        assert self.state.chat_mode is False
        
        # Toggle to True
        result = self.state.toggle_chat_mode()
        assert result is True
        assert self.state.chat_mode is True
        
        # Toggle back to False
        result = self.state.toggle_chat_mode()
        assert result is False
        assert self.state.chat_mode is False
    
    def test_get_recent_commands(self):
        """Test getting recent commands with limit"""
        for i in range(20):
            self.state.add_command(f"cmd_{i}")
        
        # Get last 5 commands
        recent = self.state.get_recent_commands(5)
        assert len(recent) == 5
        assert recent == ["cmd_15", "cmd_16", "cmd_17", "cmd_18", "cmd_19"]
        
        # Get more than available
        recent = self.state.get_recent_commands(30)
        assert len(recent) == 20  # All available commands
```

### Testing Command Handler

```python
# tests/test_command_handler.py
import pytest
from unittest.mock import patch, Mock
from src.command_handler import CommandHandler, CommandResult

class TestCommandHandler:
    def setup_method(self):
        self.handler = CommandHandler()
    
    def test_empty_command(self):
        """Test execution of empty command"""
        result = self.handler.execute("")
        assert isinstance(result, CommandResult)
        assert result.exit_code == 0
        assert result.stdout == ""
        assert result.stderr == ""
    
    @patch('subprocess.run')
    def test_successful_command(self, mock_run):
        """Test successful command execution"""
        # Mock successful subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "file1.txt\nfile2.txt\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.handler.execute("ls")
        
        assert isinstance(result, CommandResult)
        assert result.exit_code == 0
        assert "file1.txt" in result.stdout
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_failed_command(self, mock_run):
        """Test failed command execution"""
        # Mock failed subprocess result
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "command not found"
        mock_run.return_value = mock_result
        
        result = self.handler.execute("nonexistent_command")
        
        assert isinstance(result, CommandResult)
        assert result.exit_code == 1
        assert "command not found" in result.stderr
        assert self.handler.last_exit_code == 1
    
    @patch('os.chdir')
    @patch('os.path.expanduser')
    def test_cd_command_success(self, mock_expanduser, mock_chdir):
        """Test successful cd command"""
        mock_expanduser.return_value = "/home/user"
        
        result = self.handler.execute("cd /home/user")
        
        mock_chdir.assert_called_with("/home/user")
        assert result.exit_code == 0
        assert self.handler.last_exit_code == 0
    
    @patch('os.chdir')
    def test_cd_command_failure(self, mock_chdir):
        """Test cd command with non-existent directory"""
        mock_chdir.side_effect = FileNotFoundError()
        
        result = self.handler.execute("cd /nonexistent")
        
        assert result.exit_code == 1
        assert "no such file or directory" in result.stderr
        assert self.handler.last_exit_code == 1
    
    def test_cd_no_args(self):
        """Test cd command without arguments"""
        with patch('os.chdir') as mock_chdir:
            with patch('os.path.expanduser', return_value="/home/user"):
                result = self.handler.execute("cd")
                
                mock_chdir.assert_called_with("/home/user")
                assert result.exit_code == 0
    
    @patch('subprocess.run')
    def test_subprocess_exception(self, mock_run):
        """Test handling of subprocess exceptions"""
        mock_run.side_effect = Exception("Subprocess error")
        
        result = self.handler.execute("some_command")
        
        assert result.exit_code == 1
        assert "Command execution failed" in result.stderr
        assert self.handler.last_exit_code == 1
```

### Testing Configuration System

```python
# tests/test_config.py
import pytest
import json
import tempfile
from pathlib import Path
from src.config import Config, c_DEFAULT_CONFIG

class TestConfig:
    def test_config_with_nonexistent_file(self):
        """Test config creation when file doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config = Config(str(config_path))
            
            # Should create file with defaults
            assert config_path.exists()
            assert config.get('ai.model') == 'llama2'
            assert config.get('terminal.history_size') == 1000
    
    def test_config_with_existing_file(self):
        """Test config loading from existing file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            # Create config file with custom values
            custom_config = {
                "ai": {"model": "codellama", "enabled": False},
                "terminal": {"history_size": 500}
            }
            with open(config_path, 'w') as f:
                json.dump(custom_config, f)
            
            config = Config(str(config_path))
            
            # Should load custom values
            assert config.get('ai.model') == 'codellama'
            assert config.get('ai.enabled') is False
            assert config.get('terminal.history_size') == 500
            
            # Should still have defaults for missing keys
            assert config.get('ai.base_url') == 'http://localhost:11434'
    
    def test_config_merge_with_defaults(self):
        """Test merging user config with new defaults"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            # Create incomplete config
            partial_config = {"ai": {"model": "mistral"}}
            with open(config_path, 'w') as f:
                json.dump(partial_config, f)
            
            config = Config(str(config_path))
            
            # Should have user setting
            assert config.get('ai.model') == 'mistral'
            
            # Should have default for missing settings
            assert config.get('ai.enabled') is True
            assert config.get('terminal.history_size') == 1000
    
    def test_dot_notation_get(self):
        """Test dot notation for getting values"""
        config = Config()
        
        # Test nested access
        assert config.get('ai.model') == 'llama2'
        assert config.get('ai.base_url') == 'http://localhost:11434'
        
        # Test with default
        assert config.get('nonexistent.key', 'default') == 'default'
        
        # Test missing key without default
        assert config.get('nonexistent.key') is None
    
    def test_dot_notation_set(self):
        """Test dot notation for setting values"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config = Config(str(config_path))
            
            # Set nested value
            config.set('ai.model', 'new_model')
            assert config.get('ai.model') == 'new_model'
            
            # Set deeply nested value
            config.set('new.section.value', 'test')
            assert config.get('new.section.value') == 'test'
    
    def test_config_save(self):
        """Test saving configuration to file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config = Config(str(config_path))
            
            # Modify and save
            config.set('ai.model', 'test_model')
            config.save()
            
            # Reload and verify
            new_config = Config(str(config_path))
            assert new_config.get('ai.model') == 'test_model'
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON config file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            
            # Write invalid JSON
            with open(config_path, 'w') as f:
                f.write("{ invalid json }")
            
            # Should use defaults and warn
            config = Config(str(config_path))
            assert config.get('ai.model') == 'llama2'  # Default value
```

### Testing AI Integration

```python
# tests/test_ollama_helper.py
import pytest
import requests
from unittest.mock import Mock, patch
from src.ollama_helper import OllamaHelper
from src.config import Config

class TestOllamaHelper:
    def setup_method(self):
        self.config = Mock(spec=Config)
        self.config.get_ollama_url.return_value = "http://localhost:11434"
        self.config.get_ollama_model.return_value = "llama2"
        self.ollama = OllamaHelper(self.config)
    
    @patch('requests.request')
    def test_is_available_success(self, mock_request):
        """Test Ollama availability check when service is running"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        result = self.ollama.is_available()
        
        assert result is True
        mock_request.assert_called_once()
    
    @patch('requests.request')
    def test_is_available_failure(self, mock_request):
        """Test Ollama availability check when service is down"""
        mock_request.side_effect = requests.RequestException()
        
        result = self.ollama.is_available()
        
        assert result is False
    
    @patch('os.path.exists')
    def test_detect_context_git_repo(self, mock_exists):
        """Test context detection in git repository"""
        mock_exists.side_effect = lambda path: path == '.git'
        
        context = self.ollama._detect_context()
        
        assert context['is_git_repo'] is True
        assert context['is_node_project'] is False
        assert context['is_python_project'] is False
        assert context['is_docker_project'] is False
    
    @patch('os.path.exists')
    def test_detect_context_node_project(self, mock_exists):
        """Test context detection in Node.js project"""
        mock_exists.side_effect = lambda path: path == 'package.json'
        
        context = self.ollama._detect_context()
        
        assert context['is_git_repo'] is False
        assert context['is_node_project'] is True
        assert context['is_python_project'] is False
        assert context['is_docker_project'] is False
    
    @patch('os.path.exists')
    def test_detect_context_python_project(self, mock_exists):
        """Test context detection in Python project"""
        mock_exists.side_effect = lambda path: path in ['requirements.txt', 'pyproject.toml']
        
        context = self.ollama._detect_context()
        
        assert context['is_python_project'] is True
    
    def test_create_smart_prompt_git_context(self):
        """Test smart prompt creation for git commands"""
        context = {'is_git_repo': True}
        
        prompt = self.ollama._create_smart_prompt('git status', context)
        
        assert 'git repository' in prompt.lower()
        assert 'git status' in prompt
    
    def test_create_smart_prompt_generic(self):
        """Test smart prompt creation for generic commands"""
        context = {'is_git_repo': False, 'is_node_project': False}
        
        prompt = self.ollama._create_smart_prompt('ls', context)
        
        assert 'ls' in prompt
        assert '2-3 most useful examples' in prompt
    
    @patch('requests.post')
    def test_get_help_success(self, mock_post):
        """Test successful help generation"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {"response": "ls lists directory contents"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        with patch.object(self.ollama, 'is_available', return_value=True):
            result = self.ollama.get_help('ls')
        
        assert "ls lists directory contents" in result
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_get_help_timeout(self, mock_post):
        """Test help generation timeout"""
        mock_post.side_effect = requests.Timeout()
        
        with patch.object(self.ollama, 'is_available', return_value=True):
            result = self.ollama.get_help('ls')
        
        assert "timeout" in result.lower()
        assert "man ls" in result
    
    def test_get_help_service_unavailable(self):
        """Test help generation when service is unavailable"""
        with patch.object(self.ollama, 'is_available', return_value=False):
            result = self.ollama.get_help('ls')
        
        assert "ollama not available" in result.lower()
    
    def test_help_caching(self):
        """Test help response caching"""
        with patch.object(self.ollama, 'is_available', return_value=True):
            with patch('requests.post') as mock_post:
                mock_response = Mock()
                mock_response.json.return_value = {"response": "cached response"}
                mock_response.raise_for_status.return_value = None
                mock_post.return_value = mock_response
                
                # First call should hit API
                result1 = self.ollama.get_help('ls')
                assert mock_post.call_count == 1
                
                # Second call should use cache
                result2 = self.ollama.get_help('ls')
                assert mock_post.call_count == 1  # No additional API call
                assert result1 == result2
    
    def test_cache_size_limit(self):
        """Test cache size limitation"""
        self.ollama._help_cache = {}
        
        # Fill cache beyond limit
        for i in range(25):  # More than 20 item limit
            cache_key = f"help_cmd{i}_/tmp"
            self.ollama._help_cache[cache_key] = f"response{i}"
        
        # Simulate cache cleanup
        if len(self.ollama._help_cache) > 20:
            self.ollama._help_cache.pop(next(iter(self.ollama._help_cache)))
        
        assert len(self.ollama._help_cache) <= 20
```

## Integration Testing

### End-to-End Testing

```python
# tests/test_integration.py
import pytest
import subprocess
import time
import requests
from pathlib import Path

class TestIntegration:
    def setup_method(self):
        """Setup for integration tests"""
        # Ensure Ollama is running
        self.ensure_ollama_running()
        
        # Setup test environment
        self.test_env = {
            'TERMSAGE_CONFIG_DIR': str(Path.home() / '.termsage-test'),
            'TERMSAGE_AI_MODEL': 'llama2:7b'
        }
    
    def ensure_ollama_running(self):
        """Ensure Ollama service is available for testing"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        
        # Try to start Ollama
        try:
            subprocess.run(['ollama', 'serve'], check=False, timeout=5)
            time.sleep(2)  # Give it time to start
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Ollama not available for integration tests")
    
    def run_termsage_command(self, command: str, timeout: int = 30):
        """Run a command in TermSage and capture output"""
        cmd = ['python', 'src/main.py']
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, **self.test_env}
        )
        
        try:
            stdout, stderr = process.communicate(
                input=f"{command}\nexit\n", 
                timeout=timeout
            )
            return stdout, stderr, process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            pytest.fail(f"Command '{command}' timed out")
    
    def test_help_command_integration(self):
        """Test help command end-to-end"""
        stdout, stderr, returncode = self.run_termsage_command("help")
        
        assert returncode == 0
        assert "TermSage Help" in stdout
        assert "QUICK START" in stdout
        assert "/chat" in stdout
    
    def test_ai_help_integration(self):
        """Test AI help functionality end-to-end"""
        stdout, stderr, returncode = self.run_termsage_command("ls?")
        
        assert returncode == 0
        # Should contain AI response
        assert "💡" in stdout or "🤖" in stdout
    
    def test_chat_mode_integration(self):
        """Test chat mode functionality"""
        commands = "/chat\nHello\n/exit"
        stdout, stderr, returncode = self.run_termsage_command(commands)
        
        assert returncode == 0
        assert "Entered chat mode" in stdout
        assert "Exited chat mode" in stdout
    
    def test_model_switching_integration(self):
        """Test model switching functionality"""
        stdout, stderr, returncode = self.run_termsage_command("/models")
        
        assert returncode == 0
        assert "Installed Ollama models" in stdout or "models" in stdout.lower()
    
    def test_config_display_integration(self):
        """Test configuration display"""
        stdout, stderr, returncode = self.run_termsage_command("/config")
        
        assert returncode == 0
        assert "Configuration" in stdout or "{" in stdout  # JSON config
    
    def test_command_execution_integration(self):
        """Test normal command execution"""
        stdout, stderr, returncode = self.run_termsage_command("echo 'test'")
        
        assert returncode == 0
        assert "test" in stdout
    
    def test_error_handling_integration(self):
        """Test error handling for failed commands"""
        stdout, stderr, returncode = self.run_termsage_command("nonexistent_command_xyz")
        
        assert returncode == 0  # TermSage should continue running
        # Should show error or suggestion
        assert "command not found" in stdout or "not found" in stderr
```

### Performance Testing

```python
# tests/test_performance.py
import pytest
import time
import psutil
import os
from src.main import main
from src.ollama_helper import OllamaHelper
from src.config import Config

class TestPerformance:
    def setup_method(self):
        self.config = Config()
        self.ollama = OllamaHelper(self.config)
    
    def test_startup_time(self):
        """Test application startup performance"""
        start_time = time.time()
        
        # Import and initialize main components
        from src.main import main
        from src.command_handler import CommandHandler
        from src.command_registry import CommandRegistry
        from src.ui_utils import UIUtils
        
        config = Config()
        command_handler = CommandHandler()
        ui = UIUtils()
        
        elapsed = time.time() - start_time
        
        # Startup should be under 1 second
        assert elapsed < 1.0
    
    def test_ai_response_time(self):
        """Test AI response time performance"""
        if not self.ollama.is_available():
            pytest.skip("Ollama not available for performance testing")
        
        start_time = time.time()
        response = self.ollama.get_help("ls")
        elapsed = time.time() - start_time
        
        # AI responses should complete within 10 seconds
        assert elapsed < 10.0
        assert len(response) > 0
    
    def test_cache_performance(self):
        """Test caching performance improvement"""
        if not self.ollama.is_available():
            pytest.skip("Ollama not available for cache testing")
        
        # First call (uncached)
        start_time = time.time()
        response1 = self.ollama.get_help("git")
        first_call_time = time.time() - start_time
        
        # Second call (cached)
        start_time = time.time()
        response2 = self.ollama.get_help("git")
        second_call_time = time.time() - start_time
        
        # Cached call should be much faster
        assert second_call_time < 0.1  # Under 100ms
        assert second_call_time < first_call_time / 10  # At least 10x faster
        assert response1 == response2  # Same content
    
    def test_memory_usage(self):
        """Test memory usage stays reasonable"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform memory-intensive operations
        ollama = OllamaHelper(self.config)
        for i in range(50):
            if ollama.is_available():
                ollama.get_help(f"command_{i % 5}")  # Reuse some commands for caching
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024
    
    def test_command_processing_speed(self):
        """Test command processing performance"""
        from src.command_registry import CommandRegistry, AppState
        from src.ui_utils import UIUtils
        
        ui = UIUtils()
        registry = CommandRegistry(ui, None, None, self.ollama, self.config)
        state = AppState()
        registry.set_state(state)
        
        # Test command routing speed
        start_time = time.time()
        for _ in range(1000):
            result = registry.execute("unknown_command")
            assert result is None  # Should return quickly for unknown commands
        elapsed = time.time() - start_time
        
        # 1000 command routes should take less than 0.1 seconds
        assert elapsed < 0.1
    
    def benchmark_ai_operations(self):
        """Benchmark different AI operations"""
        if not self.ollama.is_available():
            pytest.skip("Ollama not available for benchmarking")
        
        operations = {
            'help_short': lambda: self.ollama.get_help('ls'),
            'help_long': lambda: self.ollama.get_help('docker run --help'),
            'chat_simple': lambda: self.ollama.chat('Hello'),
            'chat_complex': lambda: self.ollama.chat('Explain how to set up a Python development environment'),
        }
        
        results = {}
        for op_name, operation in operations.items():
            start_time = time.time()
            result = operation()
            elapsed = time.time() - start_time
            
            results[op_name] = {
                'time': elapsed,
                'response_length': len(result)
            }
        
        # Print benchmark results
        print("\nAI Operation Benchmarks:")
        for op_name, data in results.items():
            print(f"{op_name}: {data['time']:.2f}s ({data['response_length']} chars)")
        
        # Basic performance assertions
        assert results['help_short']['time'] < 5.0
        assert results['chat_simple']['time'] < 10.0
```

## Debugging Techniques

### Debugging TermSage Issues

**1. Enable Debug Logging**
```bash
# Run with debug output
TERMSAGE_DEBUG=true python src/main.py

# Or modify code temporarily
import logging
logging.basicConfig(level=logging.DEBUG)
```

**2. Interactive Debugging**
```python
# Add breakpoints in code
import pdb; pdb.set_trace()

# Or use ipdb for better interface
import ipdb; ipdb.set_trace()

# Remote debugging with remote-pdb
import remote_pdb; remote_pdb.set_trace()
```

**3. Component Isolation**
```python
# Test individual components
from src.config import Config
from src.ollama_helper import OllamaHelper

config = Config()
print(f"Config loaded: {config.settings}")

ollama = OllamaHelper(config)
print(f"Ollama available: {ollama.is_available()}")
print(f"Current model: {ollama.current_model}")
```

**4. AI Integration Debugging**
```bash
# Test Ollama directly
curl http://localhost:11434/api/tags
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Test prompt",
  "stream": false
}'

# Check Ollama logs
journalctl -u ollama -f

# List installed models
ollama list
```

### Common Debugging Scenarios

**Problem: Commands not being recognized**
```python
# Debug command registry
registry = CommandRegistry(ui, help_system, onboarding, ollama, config)
print(f"Registered commands: {list(registry.commands.keys())}")
print(f"Pattern commands: {list(registry.pattern_commands.keys())}")

# Test command matching
result = registry.execute("your_command")
print(f"Command result: {result}")
```

**Problem: AI not responding**
```python
# Debug AI connectivity
ollama = OllamaHelper(config)
print(f"Base URL: {ollama.base_url}")
print(f"Available: {ollama.is_available()}")
print(f"Model test: {ollama.test_model()}")

# Test manual request
import requests
response = requests.get(f"{ollama.base_url}/api/tags", timeout=5)
print(f"API response: {response.status_code}")
```

**Problem: Configuration not loading**
```python
# Debug configuration
config = Config()
print(f"Config path: {config.config_path}")
print(f"Config exists: {config.config_path.exists()}")
print(f"Config contents: {config.settings}")

# Test specific values
print(f"AI model: {config.get('ai.model')}")
print(f"AI enabled: {config.get('ai.enabled')}")
```

### Testing Tools and Utilities

**Custom Test Utilities**
```python
# tests/utils.py
import tempfile
import json
from pathlib import Path
from src.config import Config

def create_test_config(config_data: dict) -> Config:
    """Create a temporary config for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    return Config(temp_path)

def mock_ollama_response(response_text: str):
    """Create a mock Ollama response"""
    from unittest.mock import Mock
    mock_response = Mock()
    mock_response.json.return_value = {"response": response_text}
    mock_response.raise_for_status.return_value = None
    return mock_response

class TermSageTestHelper:
    """Helper class for TermSage testing"""
    
    def __init__(self):
        self.temp_dirs = []
    
    def create_temp_config_dir(self):
        """Create temporary config directory"""
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        return Path(temp_dir)
    
    def cleanup(self):
        """Clean up temporary directories"""
        import shutil
        for temp_dir in self.temp_dirs:
            shutil.rmtree(temp_dir, ignore_errors=True)
        self.temp_dirs.clear()
    
    def assert_ai_response_format(self, response: str):
        """Assert AI response follows expected format"""
        assert isinstance(response, str)
        assert len(response) > 0
        # Add more format assertions as needed
```

## Test Automation and CI/CD

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml
name: Test TermSage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-mock
    
    - name: Install Ollama
      run: |
        curl -fsSL https://ollama.ai/install.sh | sh
        ollama serve &
        sleep 5
        ollama pull llama2:7b
    
    - name: Run unit tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/test_integration.py -v
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

### Test Coverage Requirements

**Coverage Goals**:
- Unit tests: > 80% code coverage
- Critical paths: 100% coverage (command routing, AI integration)
- Error handling: All error paths tested
- Configuration: All config options tested

**Generate Coverage Report**:
```bash
# Run tests with coverage
pytest --cov=src --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

This comprehensive testing guide ensures TermSage maintains high quality and reliability while enabling confident development and debugging.
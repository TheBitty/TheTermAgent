# Coding Conventions

## Overview
This document outlines the coding standards, design patterns, and architectural guidelines for the TermSage project. Following these conventions ensures consistency, maintainability, and quality across the codebase.

## Language-Specific Conventions

### Python (Primary Language)

#### Naming Conventions
- **Global Variables**: `g_VARIABLE_NAME` (e.g., `g_TERMINAL_CONFIG`, `g_AI_MODELS`)
- **Constants**: `c_CONSTANT_NAME` (e.g., `c_MAX_RETRIES`, `c_TIMEOUT_SECONDS`)
- **Classes**: `PascalCase` (e.g., `TerminalHandler`, `AIAssistant`)
- **Functions**: `snake_case` (e.g., `execute_command`, `parse_input`)
- **Instance Variables**: `snake_case` (e.g., `command_history`, `current_model`)
- **Private Members**: `_variable_name` (e.g., `_internal_state`, `_cache`)
- **Function Parameters**: `snake_case` (e.g., `user_input`, `model_name`)
- **Module Names**: `lowercase_with_underscores.py`

#### Code Style
- Follow PEP 8 guidelines
- Maximum line length: 100 characters
- Use type hints for function parameters and returns
- Docstrings for all public functions and classes

#### Example:
```python
from typing import List, Optional, Dict

# Constants
c_DEFAULT_TIMEOUT = 30
c_MAX_RETRIES = 3

# Global configuration
g_TERMINAL_CONFIG = None

class TerminalAgent:
    """Main terminal agent handling user interactions."""
    
    def __init__(self, config_path: str):
        """Initialize the terminal agent.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self._session_history: List[str] = []
    
    def execute_command(self, user_input: str) -> Dict[str, any]:
        """Execute user command with safety checks.
        
        Args:
            user_input: Raw command from user
            
        Returns:
            Dictionary containing exit_code, stdout, stderr
        """
        # Implementation here
        pass
```

## Architecture Patterns

### 1. Separation of Concerns
- **Presentation Layer**: Terminal UI and user interaction
- **Business Logic**: Command processing and AI integration
- **Data Layer**: Configuration and history management

### 2. Error Handling
```python
try:
    result = risky_operation()
except SpecificError as e:
    # Handle specific error
    logger.error(f"Operation failed: {e}")
    return fallback_value
except Exception as e:
    # Log unexpected errors
    logger.exception("Unexpected error")
    raise
finally:
    # Cleanup resources
    cleanup()
```

### 3. Async Operations
- Use `asyncio` for non-blocking AI calls
- Maintain responsive terminal during AI operations
- Implement proper timeout handling

### 4. Dependency Injection
```python
class CommandHandler:
    def __init__(self, executor: CommandExecutor, 
                 validator: CommandValidator):
        self.executor = executor
        self.validator = validator
```

## Project Structure
```
TermAgent/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── command_handler.py # Command processing
│   ├── config.py          # Configuration
│   └── ai/                # AI-related modules
│       ├── __init__.py
│       ├── models.py
│       └── providers.py
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── config/              # Configuration files
```

## Testing Standards

### Test Organization
- Mirror source code structure in tests
- One test file per source file
- Use descriptive test names

### Test Patterns
```python
import pytest
from unittest.mock import Mock, patch

class TestCommandHandler:
    """Test cases for CommandHandler."""
    
    def test_execute_valid_command(self):
        """Should execute valid commands successfully."""
        # Arrange
        handler = CommandHandler()
        command = "ls -la"
        
        # Act
        result = handler.execute(command)
        
        # Assert
        assert result.exit_code == 0
        assert result.stdout is not None
    
    @pytest.mark.parametrize("command,expected", [
        ("rm -rf /", True),
        ("ls", False),
    ])
    def test_is_dangerous_command(self, command, expected):
        """Should identify dangerous commands."""
        assert is_dangerous(command) == expected
```

## Security Guidelines

### Input Validation
- Always sanitize user input
- Validate command arguments
- Use parameterized queries for any database operations

### Secrets Management
- Never hardcode credentials
- Use environment variables or secure vaults
- Implement proper key rotation

### Command Execution
```python
# Safe command execution
import shlex
import subprocess

def safe_execute(command: str) -> subprocess.CompletedProcess:
    """Execute command with proper escaping."""
    # Parse and validate
    args = shlex.split(command)
    
    # Check against whitelist/blacklist
    if is_dangerous_command(args[0]):
        raise SecurityError("Command not allowed")
    
    # Execute with timeout
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=c_COMMAND_TIMEOUT
    )
```

## Performance Guidelines

### Resource Management
- Close file handles and connections properly
- Implement connection pooling for APIs
- Use context managers for resource cleanup

### Caching Strategy
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_command_help(command: str) -> str:
    """Cache command help lookups."""
    return fetch_help_from_ai(command)
```

### Profiling
- Profile before optimizing
- Focus on bottlenecks
- Measure impact of changes

## Documentation Standards

### Code Documentation
- All public APIs must have docstrings
- Include examples for complex functions
- Document exceptions and edge cases

### README Requirements
- Installation instructions
- Quick start guide
- API reference
- Contributing guidelines

## Git Workflow

### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `refactor/description` - Code improvements
- `docs/description` - Documentation updates

### Commit Messages
```
type(scope): subject

body (optional)

footer (optional)
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Process
1. Create feature branch
2. Write tests
3. Implement feature
4. Update documentation
5. Submit PR with description
6. Address review feedback

## Tools and Automation

### Linting
- `pylint` for Python code analysis
- `black` for code formatting
- `isort` for import sorting
- `mypy` for type checking

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

## Evolution Notes
- Review and update conventions quarterly
- Document architectural decisions
- Maintain backwards compatibility
- Deprecate features gracefully
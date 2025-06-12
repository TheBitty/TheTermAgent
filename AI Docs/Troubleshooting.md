# Troubleshooting Guide

## Overview
This document contains common issues encountered in the TermSage project, their solutions, and debugging strategies. It serves as a first-line reference for resolving problems quickly.

## Common Issues and Solutions

### 1. Terminal Issues

#### Issue: Commands not executing
**Symptoms**: Commands entered in terminal don't produce output or hang indefinitely

**Solutions**:
1. Check if subprocess is properly initialized
2. Verify command permissions
3. Check for blocking I/O operations

**Debug Steps**:
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In command execution
logger.debug(f"Executing command: {command}")
result = subprocess.run(command, shell=True, capture_output=True)
logger.debug(f"Exit code: {result.returncode}")
logger.debug(f"Stdout: {result.stdout}")
logger.debug(f"Stderr: {result.stderr}")
```

#### Issue: Terminal encoding errors
**Symptoms**: Unicode decode errors, garbled output

**Solutions**:
```python
# Force UTF-8 encoding
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# In subprocess calls
result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace'
)
```

### 2. AI Integration Issues

#### Issue: AI model not responding
**Symptoms**: AI features don't work, timeouts

**Solutions**:
1. Verify AI service is running (for Ollama: `curl http://localhost:11434/api/tags`)
2. Check API keys for external services
3. Implement fallback providers

**Debug Steps**:
```python
# Test AI connectivity
async def test_ai_connection():
    try:
        response = await ai_provider.test_connection()
        print(f"AI Provider Status: {response}")
    except Exception as e:
        print(f"AI Connection Failed: {e}")
        # Try fallback
        fallback_provider = get_fallback_provider()
        return await fallback_provider.connect()
```

#### Issue: AI responses too slow
**Symptoms**: Long delays when using AI features

**Solutions**:
1. Implement streaming responses
2. Use smaller models for simple tasks
3. Add caching for common queries
4. Set appropriate timeouts

```python
# Streaming implementation
async def stream_ai_response(prompt: str):
    async for chunk in ai_provider.stream_complete(prompt):
        yield chunk
        # Process chunk immediately
```

### 3. Auto-completion Issues

#### Issue: Tab completion not working
**Symptoms**: Pressing Tab doesn't show suggestions

**Solutions**:
1. Check readline configuration
2. Verify completion function is registered
3. Debug completion callback

```python
# Debug completion
def debug_completer(text, state):
    print(f"Completing: '{text}', state: {state}")
    matches = get_completions(text)
    print(f"Matches: {matches}")
    return matches[state] if state < len(matches) else None

readline.set_completer(debug_completer)
```

### 4. Configuration Issues

#### Issue: Config file not loading
**Symptoms**: Default settings used instead of custom config

**Solutions**:
1. Check file path and permissions
2. Validate JSON/YAML syntax
3. Implement config validation

```python
# Config validation
import json
import jsonschema

def validate_config(config_path: str):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Validate against schema
        jsonschema.validate(config, CONFIG_SCHEMA)
        return config
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        return DEFAULT_CONFIG
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config: {e}")
        return DEFAULT_CONFIG
```

### 5. Performance Issues

#### Issue: Terminal feels sluggish
**Symptoms**: Delays in command execution, slow response

**Solutions**:
1. Profile code to find bottlenecks
2. Implement async operations
3. Optimize AI calls

```python
# Performance profiling
import cProfile
import pstats

def profile_function(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return result
    return wrapper
```

### 6. Cross-Platform Issues

#### Issue: Works on Linux but not Windows
**Symptoms**: Platform-specific errors

**Solutions**:
```python
import platform
import os

# Platform-specific handling
if platform.system() == 'Windows':
    # Windows-specific code
    shell = True
    path_separator = ';'
else:
    # Unix-like systems
    shell = False
    path_separator = ':'

# Use pathlib for cross-platform paths
from pathlib import Path
config_path = Path.home() / '.termsage' / 'config.json'
```

## Debugging Strategies

### 1. Enable Verbose Logging
```python
# In main.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
```

### 2. Interactive Debugging
```python
# Add breakpoints
import pdb

def problematic_function():
    # ... code ...
    pdb.set_trace()  # Debugger stops here
    # ... more code ...
```

### 3. Error Context Collection
```python
def collect_debug_info():
    """Collect system information for bug reports."""
    info = {
        'platform': platform.platform(),
        'python_version': sys.version,
        'termsage_version': __version__,
        'environment': dict(os.environ),
        'config': load_config(),
        'ai_providers': list_available_providers(),
    }
    return info
```

## Testing Procedures

### 1. Unit Test Failures
```bash
# Run specific test with verbose output
pytest tests/test_module.py::test_function -vvs

# Debug test with pdb
pytest tests/test_module.py --pdb
```

### 2. Integration Test Issues
```python
# Mock external dependencies
from unittest.mock import Mock, patch

@patch('requests.post')
def test_ai_integration(mock_post):
    mock_post.return_value.json.return_value = {
        'response': 'Test response'
    }
    
    result = ai_handler.process_query("test")
    assert result == "Test response"
```

## Error Messages Reference

### Common Error Patterns

#### "Permission denied"
- Check file permissions
- Verify user has necessary privileges
- Consider using sudo (with caution)

#### "Command not found"
- Verify command is installed
- Check PATH environment variable
- Use full path to executable

#### "Connection refused"
- Service not running
- Firewall blocking connection
- Wrong port/address

#### "Timeout error"
- Increase timeout values
- Check network connectivity
- Verify service responsiveness

## Maintenance Tasks

### Regular Checks
1. Clear old log files
2. Update AI model cache
3. Clean temporary files
4. Verify all services running

### Health Check Script
```python
def health_check():
    checks = {
        'terminal': check_terminal_functionality(),
        'ai_service': check_ai_connectivity(),
        'config': validate_configuration(),
        'permissions': check_file_permissions(),
    }
    
    for component, status in checks.items():
        print(f"{component}: {'✓' if status else '✗'}")
    
    return all(checks.values())
```

## Getting Help

### Log Collection
When reporting issues, include:
1. Full error message and stack trace
2. Steps to reproduce
3. System information (OS, Python version)
4. Relevant log files
5. Configuration used

### Debug Mode
Run TermSage in debug mode:
```bash
python -m termsage --debug --log-file debug.log
```

## Known Limitations

1. **Windows**: Some Unix-specific commands won't work
2. **AI Models**: Large models may require significant RAM
3. **Network**: AI features require internet for some providers
4. **Python Version**: Requires Python 3.8+

## Future Improvements
- Automated error reporting
- Self-diagnostic commands
- Performance monitoring dashboard
- Automatic recovery mechanisms
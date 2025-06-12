# Configuration Guide

## Overview
This guide covers all configuration options for TermSage, including AI providers, performance settings, safety features, and customization options.

## Configuration File Structure

### Default Configuration Location
```
~/.termsage/config.json    # User configuration
./config.user.json         # Project-specific config (git-ignored)
./config.default.json      # Default settings (do not edit)
```

### Configuration Priority
1. Command-line arguments (highest priority)
2. Environment variables
3. User configuration file
4. Project configuration file
5. Default configuration (lowest priority)

## Core Configuration

### Basic Configuration Template
```json
{
  "terminal": {
    "shell": "/bin/bash",
    "history_size": 10000,
    "timeout": 30,
    "encoding": "utf-8"
  },
  "ai": {
    "default_provider": "ollama",
    "fallback_enabled": true,
    "context_window": 4096,
    "temperature": 0.7,
    "streaming": true
  },
  "safety": {
    "command_validation": true,
    "sudo_prompt": true,
    "dangerous_commands": ["rm -rf /", "dd if=", "mkfs"],
    "resource_limits": {
      "max_memory_mb": 1024,
      "max_cpu_percent": 80,
      "max_runtime_seconds": 300
    }
  },
  "ui": {
    "theme": "auto",
    "show_suggestions": true,
    "autocomplete_delay_ms": 100,
    "syntax_highlighting": true
  }
}
```

## AI Provider Configuration

### Ollama (Local Models)
```json
{
  "ai": {
    "providers": {
      "ollama": {
        "enabled": true,
        "base_url": "http://localhost:11434",
        "models": {
          "default": "llama2",
          "chat": "llama2:chat",
          "code": "codellama"
        },
        "timeout": 30,
        "max_retries": 3
      }
    }
  }
}
```

### OpenAI
```json
{
  "ai": {
    "providers": {
      "openai": {
        "enabled": true,
        "api_key": "${OPENAI_API_KEY}",
        "model": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7,
        "organization": null
      }
    }
  }
}
```

### Anthropic (Claude)
```json
{
  "ai": {
    "providers": {
      "anthropic": {
        "enabled": true,
        "api_key": "${ANTHROPIC_API_KEY}",
        "model": "claude-3-opus-20240229",
        "max_tokens": 4000,
        "temperature": 0.7
      }
    }
  }
}
```

### Provider Auto-Fallback
```json
{
  "ai": {
    "fallback_enabled": true,
    "provider_priority": ["ollama", "openai", "anthropic"],
    "fallback_conditions": {
      "timeout": true,
      "rate_limit": true,
      "model_unavailable": true,
      "api_error": true
    }
  }
}
```

## Performance Configuration

### Performance Tiers
```json
{
  "performance": {
    "tier": "balanced",  // minimal, basic, balanced, high
    "tiers": {
      "minimal": {
        "ai_enabled": false,
        "autocomplete": "basic",
        "history_size": 1000
      },
      "basic": {
        "ai_enabled": true,
        "context_window": 2048,
        "autocomplete": "standard",
        "history_size": 5000
      },
      "balanced": {
        "ai_enabled": true,
        "context_window": 4096,
        "autocomplete": "enhanced",
        "history_size": 10000
      },
      "high": {
        "ai_enabled": true,
        "context_window": 8192,
        "autocomplete": "ai_powered",
        "history_size": 50000,
        "preload_models": true
      }
    }
  }
}
```

### Resource Management
```json
{
  "resources": {
    "memory": {
      "max_heap_mb": 512,
      "cache_size_mb": 128,
      "gc_threshold_mb": 256
    },
    "cpu": {
      "max_workers": 4,
      "ai_thread_priority": "low",
      "background_tasks": true
    },
    "disk": {
      "max_history_mb": 100,
      "max_cache_mb": 500,
      "temp_dir": "/tmp/termsage"
    }
  }
}
```

## Safety Configuration

### Command Validation
```json
{
  "safety": {
    "command_validation": {
      "enabled": true,
      "mode": "strict",  // permissive, standard, strict
      "whitelist": [
        "ls", "cd", "pwd", "echo", "cat", "grep", "find"
      ],
      "blacklist": [
        "rm -rf /*",
        ":(){ :|:& };:",
        "dd if=/dev/random of=/dev/sda"
      ],
      "patterns": {
        "dangerous_flags": ["-rf", "--force", "--no-preserve-root"],
        "sudo_required": ["apt", "yum", "systemctl", "service"]
      }
    }
  }
}
```

### Sandbox Mode
```json
{
  "safety": {
    "sandbox": {
      "enabled": false,
      "type": "docker",  // docker, firejail, chroot
      "image": "termsage/sandbox:latest",
      "mounts": {
        "/home/user/projects": "/workspace"
      },
      "network": "none",
      "resource_limits": {
        "memory": "512m",
        "cpu": "1.0"
      }
    }
  }
}
```

## UI Configuration

### Appearance
```json
{
  "ui": {
    "theme": {
      "mode": "auto",  // light, dark, auto
      "colors": {
        "primary": "#1e90ff",
        "success": "#32cd32",
        "warning": "#ffa500",
        "error": "#dc143c"
      },
      "prompt": {
        "format": "[{user}@{host} {cwd}]$ ",
        "git_status": true,
        "virtualenv": true
      }
    }
  }
}
```

### Auto-Completion
```json
{
  "ui": {
    "autocomplete": {
      "enabled": true,
      "trigger_chars": 2,
      "delay_ms": 100,
      "max_suggestions": 10,
      "sources": {
        "history": true,
        "files": true,
        "commands": true,
        "ai": true
      },
      "ai_settings": {
        "contextual": true,
        "learn_patterns": true,
        "confidence_threshold": 0.7
      }
    }
  }
}
```

## Environment Variables

### Supported Variables
```bash
# AI Provider Keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Configuration Overrides
export TERMSAGE_CONFIG="/path/to/config.json"
export TERMSAGE_AI_PROVIDER="ollama"
export TERMSAGE_PERFORMANCE_TIER="high"

# Feature Flags
export TERMSAGE_ENABLE_AI="true"
export TERMSAGE_ENABLE_SANDBOX="false"
export TERMSAGE_DEBUG="true"

# Resource Limits
export TERMSAGE_MAX_MEMORY="1024"
export TERMSAGE_MAX_CPU="80"
```

## Advanced Configuration

### Custom AI Prompts
```json
{
  "ai": {
    "prompts": {
      "command_help": "Explain the following command concisely: {command}",
      "error_analysis": "Analyze this error and suggest fixes: {error}",
      "autocomplete": "Suggest completions for: {partial_command}",
      "chat_system": "You are a helpful terminal assistant..."
    }
  }
}
```

### Plugin Configuration
```json
{
  "plugins": {
    "enabled": true,
    "directory": "~/.termsage/plugins",
    "autoload": ["git-helper", "docker-assistant"],
    "config": {
      "git-helper": {
        "auto_fetch": true,
        "show_branch": true
      }
    }
  }
}
```

### Logging Configuration
```json
{
  "logging": {
    "level": "INFO",  // DEBUG, INFO, WARNING, ERROR
    "file": "~/.termsage/termsage.log",
    "max_size_mb": 10,
    "rotate_count": 5,
    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    "modules": {
      "ai": "DEBUG",
      "command": "INFO",
      "ui": "WARNING"
    }
  }
}
```

## Configuration Best Practices

### 1. Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Regularly rotate API keys
- Enable command validation in production

### 2. Performance
- Start with "balanced" tier and adjust
- Monitor resource usage
- Enable caching for better response times
- Use local models when possible

### 3. Customization
- Keep user preferences in ~/.termsage/config.json
- Use project-specific config for team settings
- Document custom configurations
- Test changes in sandbox mode first

### 4. Troubleshooting
- Enable debug logging for issues
- Check provider status before reporting bugs
- Validate JSON syntax
- Use default config as reference

## Migration Guide

### From Version 1.x to 2.x
```bash
# Backup old config
cp ~/.termsage/config.json ~/.termsage/config.v1.backup.json

# Run migration tool
termsage migrate-config

# Verify new config
termsage validate-config
```

### Config Validation
```bash
# Validate configuration file
termsage validate-config /path/to/config.json

# Test configuration
termsage test-config --provider ollama

# Show effective configuration
termsage show-config --effective
```
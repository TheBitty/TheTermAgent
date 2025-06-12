# How to Use TermSage

## Quick Start

### 1. Run TermSage
```bash
cd /path/to/TermAgent
python src/main.py
```

### 2. First Time Setup
On first run, TermSage will:
- Create `~/.termsage/config.json` with default settings
- Check if Ollama is running
- Display current status

## Using the Terminal

### Regular Commands
TermSage works like any terminal:
```bash
~/Desktop/TermAgent $ ls
~/Desktop/TermAgent $ pwd
~/Desktop/TermAgent $ cd /tmp
/tmp $ echo "Hello World"
```

### AI Help (requires Ollama)
Get help for any command by adding `?`:
```bash
~/Desktop/TermAgent $ git?
🤔 Getting help for 'git' from llama2...
🤖 llama2:
Git is a distributed version control system...
[AI explanation follows]

~/Desktop/TermAgent $ docker?
🤔 Getting help for 'docker' from llama2...
🤖 llama2:
Docker is a containerization platform...
```

### Managing AI Models
List available models:
```bash
~/Desktop/TermAgent $ /models
📋 Installed Ollama models:
  ✓ llama2 (3.8GB) (current)
    mistral (4.1GB)
    codellama (7.3GB)

Current model: llama2
Switch with: /model <model_name>
```

Switch models:
```bash
~/Desktop/TermAgent $ /model mistral
✓ Switched to model: mistral
Model set to: mistral
```

### Configuration
View current config:
```bash
~/Desktop/TermAgent $ /config
Current Configuration:
{
  "terminal": {
    "history_size": 1000,
    "prompt_style": "simple"
  },
  "ai": {
    "model": "mistral",
    "enabled": true,
    "help_on_error": true,
    "base_url": "http://localhost:11434"
  }
}
```

### Special Commands
- `exit` - Exit TermSage
- `clear` - Clear screen
- `/models` - List Ollama models
- `/model <name>` - Switch model
- `/config` - Show configuration
- `<command>?` - Get AI help

## Prerequisites

### Required: Python 3.8+
```bash
python --version  # Should be 3.8 or higher
```

### Optional: Ollama (for AI features)
1. Install Ollama: https://ollama.ai
2. Start Ollama server:
   ```bash
   ollama serve
   ```
3. Install a model:
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   # or
   ollama pull codellama
   ```

## Configuration File

TermSage stores settings in `~/.termsage/config.json`:

```json
{
  "terminal": {
    "history_size": 1000,
    "prompt_style": "simple"
  },
  "ai": {
    "model": "llama2",
    "enabled": true,
    "help_on_error": true,
    "base_url": "http://localhost:11434"
  }
}
```

### Key Settings:
- `ai.model` - Default Ollama model to use
- `ai.enabled` - Enable/disable AI features
- `ai.base_url` - Ollama server URL
- `terminal.history_size` - Command history length

## Troubleshooting

### "Ollama not available"
- Make sure Ollama is installed and running: `ollama serve`
- Check if port 11434 is accessible: `curl http://localhost:11434/api/tags`

### "Model not found"
- List available models: `/models` in TermSage
- Install model: `ollama pull <model_name>`

### Config issues
- Delete config file to reset: `rm ~/.termsage/config.json`
- TermSage will recreate with defaults

### Commands not working
- Make sure you're in the right directory
- Check if command exists: `which <command>`
- Some commands might need full paths

## Examples

### Basic Usage
```bash
# Regular terminal work
~/project $ ls -la
~/project $ git status
~/project $ cd ../other-project

# Get help when needed
~/project $ git rebase?
~/project $ docker-compose?
~/project $ find?
```

### Model Management
```bash
# See what models you have
$ /models

# Try a code-specific model
$ /model codellama
$ python?  # Get Python help from codellama

# Switch to a general model
$ /model llama2
$ systemctl?  # Get system administration help
```

### Learning Workflows
```bash
# Learn new tools
$ kubernetes?
$ terraform?
$ nginx?

# Debug issues
$ npm install?  # When npm commands fail
$ permission denied?  # When you hit permission issues
```

## Tips

1. **Use specific commands**: `git push?` is better than `git?`
2. **Try different models**: Code models are better for programming questions
3. **Terminal first**: TermSage works even without AI
4. **History**: Use arrow keys for command history like normal terminals
5. **Tab completion**: Works for files and directories (basic implementation)
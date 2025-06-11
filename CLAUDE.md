# Claude Code Context - TermSage

## Project Overview
TermSage is a fully functional terminal application with built-in AI assistance. It works exactly like a regular terminal but adds intelligent auto-completion and AI help when you need it. Think of it as your normal terminal experience enhanced with AI superpowers.

## Core Concept
- **Primary Function**: Full-featured terminal that can execute any command
- **AI Enhancement**: Optional AI assistance for command suggestions, troubleshooting, and explanations
- **Smart Auto-Complete**: Context-aware command completion with AI suggestions
- **Seamless Integration**: AI help is there when you want it, invisible when you don't

## Project Structure
```
TermAgent/
├── src/                      # Core application modules
│   ├── __init__.py
│   ├── main.py              # Entry point and terminal loop
│   ├── command_handler.py   # Command execution and safety checks
│   └── config.py            # Configuration management
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_main.py         # Main test file
├── docs/                     # Documentation
│   └── building-basic-terminal.md
├── CLAUDE.md                # Project context for AI
├── README.md                # User documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata
└── setup.py                # Package setup
```

## How It Works

### Normal Terminal Usage
```bash
# Works exactly like any terminal
ls -la
cd /home/user
grep -r "pattern" .
sudo apt update
git status
python script.py
./my_script.sh
```

### AI-Enhanced Features
```bash
# Add ? to any command for AI help
nmap?          # "Explain nmap and show common usage examples"
docker?        # "Help with docker commands and best practices"
git?           # "Git command suggestions and workflows"

# AI troubleshooting when commands fail
command_that_fails  # AI automatically suggests fixes

# Chat mode for discussions
/chat          # Toggle AI chat mode
> "How do I find all files larger than 100MB?"
> "Explain this error message: permission denied"
> "What's the best way to monitor system resources?"
```

### Smart Auto-Completion
- **File/Directory Completion**: Standard tab completion for paths
- **Command Completion**: Auto-complete command names and flags
- **AI Suggestions**: Context-aware suggestions based on what you're trying to do
- **History Integration**: Learn from your command patterns

## Key Commands

### Terminal Operations
```bash
# Standard terminal functionality
any_command [args]    # Execute any system command
cd [path]            # Change directory
ls [options]         # List files
history              # Show command history
clear                # Clear screen
exit                 # Exit terminal
```

### AI Features
```bash
/chat                # Toggle AI chat mode
/help               # Show AI commands
/models             # List available AI models
/model <name>       # Switch AI model
/clear              # Clear AI context
command?            # Get AI help for any command
```

### Auto-Completion
- **Tab**: Standard file/command completion
- **Double-Tab**: Show all completions
- **Ctrl+Space**: Trigger AI suggestions
- **Arrow Keys**: Navigate completion menu

## Development Guidelines

### Core Principles
1. **Terminal First**: Must work as a full terminal before adding AI features
2. **Non-Intrusive AI**: AI help is optional and doesn't interfere with normal usage
3. **Performance**: Terminal operations should be fast and responsive
4. **Safety**: Prevent dangerous commands with smart validation
5. **Cross-Platform**: Work on Linux, macOS, and Windows

### Code Architecture
1. **Command Execution**: Use subprocess for reliable command execution
2. **Async Operations**: AI calls don't block terminal operations
3. **Error Handling**: Graceful fallbacks when AI is unavailable
4. **Memory Management**: Efficient context handling for long sessions
5. **Security**: Validate and sanitize all command inputs

### Code Style Guidelines

#### Variable Naming Conventions
- **Global Variables**: `g_VARIABLE_NAME` (e.g., `g_TERMINAL_CONFIG`, `g_AI_MODELS`)
- **Constants**: `c_CONSTANT_NAME` (e.g., `c_MAX_RETRIES`, `c_TIMEOUT_SECONDS`)
- **Class Variables**: `PascalCase` (e.g., `TerminalHandler`, `AIAssistant`)
- **Instance Variables**: `snake_case` (e.g., `command_history`, `current_model`)
- **Private Variables**: `_variable_name` (e.g., `_internal_state`, `_cache`)
- **Function Parameters**: `snake_case` (e.g., `user_input`, `model_name`)

#### Example Usage
```python
# Constants
c_DEFAULT_MODEL = "ollama"
c_MAX_CONTEXT_LENGTH = 4096
c_COMMAND_TIMEOUT = 30

# Global variables
g_CURRENT_SESSION = None
g_AI_PROVIDER = None

# Class example
class TerminalAgent:
    def __init__(self, config_path):
        self.config_path = config_path
        self._internal_buffer = []
        
    def execute_command(self, user_input):
        # Implementation here
        pass
```

### AI Integration Points
1. **Command Suggestions**: When user types `command?`
2. **Failure Analysis**: When commands return non-zero exit codes
3. **Chat Mode**: For general discussions and explanations
4. **Auto-Completion**: Enhanced tab completion with AI context

## Configuration

### AI Providers
- **Ollama**: Local models for privacy (primary)
- **OpenAI**: GPT models for complex reasoning
- **Anthropic**: Claude for detailed explanations
- **Auto-Fallback**: Switch providers if one is unavailable

### Performance Tiers
- **High**: Full AI features, large context windows
- **Medium**: Balanced performance and features
- **Basic**: Essential AI features only
- **Minimal**: Terminal-only mode with basic AI

### Safety Features
- **Command Validation**: Block potentially destructive commands
- **Sudo Prompts**: Extra confirmation for privileged operations
- **Resource Limits**: Prevent runaway processes
- **Sandbox Mode**: Optional isolated execution environment

## Target User Experience
"I want to use my terminal normally, but sometimes I need help with commands, explanations, or troubleshooting. The AI should be there when I need it but never get in my way during normal terminal work."

## Development Status
- ✅ Basic terminal functionality
- ✅ Command execution and safety
- ✅ AI model integration
- ✅ Auto-completion system
- 🔄 Enhanced AI suggestions
- 🔄 Cross-platform compatibility
- 📋 Advanced context management
- 📋 Performance optimizations

# AI Documentation - TermSage

## Overview
This document contains important information, context, and learnings from AI interactions with the TermSage terminal application. It serves as a persistent memory for the AI assistant to reference across chat sessions.

## Project Overview
TermSage is a fully functional terminal application with built-in AI assistance. It works exactly like a regular terminal but adds intelligent auto-completion and AI help when you need it. Think of it as your normal terminal experience enhanced with AI superpowers.

## Core Concept
- **Primary Function**: Full-featured terminal that can execute any command
- **AI Enhancement**: Optional AI assistance for command suggestions, troubleshooting, and explanations
- **Smart Auto-Complete**: Context-aware command completion with AI suggestions
- **Seamless Integration**: AI help is there when you want it, invisible when you don't

## Core Principles
1. **Terminal First**: Must work as a full terminal before adding AI features
2. **Non-Intrusive AI**: AI help is optional and doesn't interfere with normal usage
3. **Performance**: Terminal operations should be fast and responsive
4. **Safety**: Prevent dangerous commands with smart validation
5. **Cross-Platform**: Work on Linux, macOS, and Windows

## Target User Experience
"I want to use my terminal normally, but sometimes I need help with commands, explanations, or troubleshooting. The AI should be there when I need it but never get in my way during normal terminal work."

## Key Features Implemented
- Basic terminal functionality with command execution
- Safety checks for dangerous commands
- AI model integration (Ollama, OpenAI, Anthropic)
- Auto-completion system foundation
- Command help with `?` suffix (e.g., `git?`, `docker?`)
- Chat mode with `/chat` command

## Important Technical Details

### Variable Naming Conventions
- **Global Variables**: `g_VARIABLE_NAME` (e.g., `g_TERMINAL_CONFIG`)
- **Constants**: `c_CONSTANT_NAME` (e.g., `c_MAX_RETRIES`)
- **Class Variables**: `PascalCase` (e.g., `TerminalHandler`)
- **Instance Variables**: `snake_case` (e.g., `command_history`)
- **Private Variables**: `_variable_name` (e.g., `_internal_state`)

### Command Execution Flow
1. User enters command in terminal
2. Safety validation checks for dangerous operations
3. Command executed via subprocess
4. AI analyzes failures and suggests fixes
5. Results displayed to user

### AI Integration Points
1. **Command Help**: When user adds `?` to any command
2. **Error Analysis**: Automatic help when commands fail
3. **Chat Mode**: Toggle with `/chat` for discussions
4. **Auto-Complete**: Enhanced suggestions based on context

## User Interaction Patterns

### Common Use Cases
- Running system commands normally
- Getting help with complex commands (`nmap?`, `docker?`)
- Troubleshooting errors with AI assistance
- Using chat mode for explanations and learning
- Smart auto-completion for faster workflows

### Command Examples
```bash
# Normal terminal usage
ls -la
cd /home/user
git status

# AI-enhanced usage
git?                    # Get git help
docker-compose?         # Docker compose assistance
/chat                   # Enter chat mode
> "How do I find large files?"
> "Explain this error"
```

## Development Notes

### Current Status
- ✅ Basic terminal functionality
- ✅ Command execution and safety
- ✅ AI model integration
- ✅ Auto-completion system
- 🔄 Enhanced AI suggestions
- 🔄 Cross-platform compatibility
- 📋 Advanced context management
- 📋 Performance optimizations

### Key Files
- `src/main.py`: Entry point and terminal loop
- `src/command_handler.py`: Command execution and safety
- `src/config.py`: Configuration management
- `tests/test_main.py`: Test suite

### Safety Considerations
- Validates dangerous commands before execution
- Requires confirmation for sudo operations
- Implements resource limits to prevent runaway processes
- Optional sandbox mode for isolated execution

## AI Learning & Context

### Command Patterns to Remember
- Users often need help with git, docker, and system commands
- Error messages should be explained in simple terms
- Suggest alternatives when commands fail
- Learn from user's command history for better suggestions

### Response Guidelines
- Be concise in terminal mode (1-3 lines max)
- Provide detailed explanations only in chat mode
- Focus on practical solutions and examples
- Adapt to user's technical level

### Future Enhancements
- Persistent command history across sessions
- Learning from user preferences
- Custom command aliases and shortcuts
- Integration with popular development tools
- Advanced context-aware suggestions

## Session Notes
(This section will be updated with important learnings from each session)

### Session History
- [Date]: Initial documentation created
- [Date]: Add session-specific learnings here

## Important Reminders
- Always maintain terminal functionality as the primary feature
- AI features should enhance, not replace, normal terminal usage
- Performance and responsiveness are critical
- Cross-platform compatibility is essential
- User privacy and security are paramount
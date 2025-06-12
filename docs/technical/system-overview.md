# TermSage System Overview

## Introduction
TermSage is an AI-enhanced terminal emulator built in Python that provides intelligent assistance while maintaining full compatibility with standard terminal operations. This document provides a comprehensive overview of the system architecture, core components, and data flows.

## High-Level Architecture

### System Philosophy
TermSage operates as a **terminal wrapper** rather than a replacement. It intercepts user input, provides AI assistance when appropriate, and delegates actual command execution to the underlying shell through Python's subprocess system.

### Core Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    TermSage Application                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   main.py   │  │ UI System   │  │ Help System │          │
│  │(Entry Point)│  │ (ui_utils)  │  │(help_system)│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Command      │  │AI Integration│  │Config       │          │
│  │Registry     │  │(ollama_help)│  │Management   │          │
│  │(routing)    │  │             │  │(config.py)  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Command      │  │State        │  │Path         │          │
│  │Handler      │  │Management   │  │Management   │          │
│  │(execution)  │  │(AppState)   │  │(decorators) │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                    System Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │subprocess   │  │readline     │  │requests     │          │
│  │(cmd exec)   │  │(history)    │  │(AI API)     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Core Components Deep Dive

### 1. Application Entry Point (`main.py`)

**Purpose**: Application lifecycle management and coordination
**Responsibilities**:
- Initialize all system components
- Setup readline for command history and editing
- Main event loop (REPL - Read-Eval-Print Loop)
- Graceful shutdown and cleanup
- Error handling at the application level

**Key Functions**:
```python
def main():
    # Component initialization
    config = Config()
    command_handler = CommandHandler()
    ollama = OllamaHelper(config)
    ui = UIUtils()
    
    # Setup terminal environment
    setup_readline()
    print_banner()
    
    # Main event loop
    while True:
        user_input = input(get_prompt())
        # Route to appropriate handler...
```

**Startup Sequence**:
1. Load configuration from `~/.termsage/config.json`
2. Initialize AI helper and check Ollama availability
3. Setup readline with history file
4. Display banner and status information
5. Check for first-time setup needs
6. Enter main command loop

### 2. Command Registry (`command_registry.py`)

**Purpose**: Route commands to appropriate handlers
**Architecture**: Registry pattern with command mapping

**Command Types**:
- **Exact matches**: `/chat`, `/help`, `exit`, `clear`
- **Pattern matches**: `/model <name>`, commands ending with `?`
- **System commands**: Everything else goes to CommandHandler

**Routing Logic**:
```python
def execute(self, command: str) -> Optional[bool]:
    # 1. Check exact command matches
    if command.lower() in self.commands:
        return self.commands[command.lower()]()
    
    # 2. Check pattern matches  
    for pattern, handler in self.pattern_commands.items():
        if command.startswith(pattern):
            return handler(command)
    
    # 3. Check for help requests (?)
    if command.endswith("?"):
        return self.handle_help_request(command)
    
    # 4. Not a TermSage command, return None
    return None
```

**State Management Integration**:
- Maintains reference to AppState for mode switching
- Handles chat mode transitions
- Tracks command history for contextual help

### 3. Command Handler (`command_handler.py`)

**Purpose**: Execute system commands safely and capture results
**Core Responsibility**: Bridge between TermSage and the operating system

**Special Handling**:
- **`cd` commands**: Must change Python process directory
- **Output capture**: Both stdout and stderr for AI analysis
- **Exit codes**: Track success/failure for error handling
- **Shell features**: Support pipes, redirects, and shell operators

**Execution Flow**:
```python
def execute(self, command: str) -> CommandResult:
    # Special case: cd command
    if command.startswith("cd "):
        return self._handle_cd(command)
    
    # Execute via subprocess
    result = subprocess.run(
        command,
        shell=True,  # Enable shell features
        capture_output=True,
        text=True,
        cwd=os.getcwd()  # Use current directory
    )
    
    # Display output immediately
    if result.stdout:
        print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='')
    
    # Return result for AI analysis
    return CommandResult(
        stdout=result.stdout,
        stderr=result.stderr, 
        exit_code=result.returncode
    )
```

### 4. AI Integration (`ollama_helper.py`)

**Purpose**: Interface with Ollama for AI-powered assistance
**Key Features**:
- Context-aware help generation
- Error analysis and suggestions
- Interactive chat functionality
- Model management and switching

**Context Detection**:
```python
def _detect_context(self) -> dict:
    return {
        'is_git_repo': os.path.exists('.git'),
        'is_node_project': os.path.exists('package.json'), 
        'is_python_project': os.path.exists('requirements.txt') or os.path.exists('pyproject.toml'),
        'is_docker_project': os.path.exists('Dockerfile'),
        'current_dir': os.path.basename(os.getcwd())
    }
```

**Smart Prompting System**:
Different prompt templates based on context:
- Git repositories get git-specific help
- Node.js projects get npm-focused assistance
- Python projects get pip/virtualenv guidance
- Generic commands get universal examples

**Performance Optimizations**:
- **Response Caching**: LRU cache with 20-item limit
- **Timeout Management**: Different timeouts for different operations
- **Token Limiting**: Reduced response lengths for faster processing
- **Connection Pooling**: Reuse HTTP connections to Ollama

### 5. Configuration System (`config.py`)

**Purpose**: Manage application settings with flexibility and defaults
**Features**:
- JSON-based configuration with dot notation access
- Automatic default value merging
- Environment variable overrides
- Graceful handling of missing/invalid config

**Configuration Loading Strategy**:
```python
def _load_config(self) -> Dict[str, Any]:
    # 1. Check if config file exists
    if self.config_path.exists():
        # Load and merge with defaults
        user_config = json.load(open(self.config_path))
        merged = self._merge_configs(DEFAULT_CONFIG, user_config)
        
        # Save back if new defaults were added
        if merged != user_config:
            self._save_config(merged)
        
        return merged
    else:
        # First run: create config with defaults
        self._save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
```

**Dot Notation Access**:
```python
config.get('ai.model')           # Returns "llama2"
config.get('ai.timeout.help')    # Returns 15
config.set('ai.model', 'mistral') # Updates nested value
```

### 6. UI System (`ui_utils.py`)

**Purpose**: Consistent terminal formatting and visual feedback
**Features**:
- ANSI color support with fallback
- Loading indicators for long operations
- Consistent message formatting
- Terminal capability detection

**Color Support Detection**:
```python
def _supports_color(self) -> bool:
    return (
        hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
        'TERM' in os.environ and os.environ['TERM'] != 'dumb'
    )
```

**Message Types**:
- Success: ✓ green
- Error: ✗ red  
- Warning: ⚠ yellow
- Info: ℹ blue
- AI Response: 🤖 cyan

### 7. State Management (`command_registry.py` - AppState class)

**Purpose**: Track application state across command executions
**State Components**:
- Current mode (normal/chat)
- Recent command history (last 50 commands)
- Command count for tip frequency
- Session context for AI conversations

**State Transitions**:
```python
class AppState:
    def __init__(self):
        self.chat_mode = False
        self.recent_commands = []
        self.command_count = 0
    
    def toggle_chat_mode(self):
        self.chat_mode = not self.chat_mode
        return self.chat_mode
    
    def add_command(self, command: str):
        self.recent_commands.append(command)
        if len(self.recent_commands) > 50:
            self.recent_commands.pop(0)
        self.command_count += 1
```

## Data Flow Analysis

### Normal Command Execution
```
User Input: "ls -la"
    ↓
main.py: get user input
    ↓
CommandRegistry.execute()
    ↓
Not a TermSage command → return None
    ↓
CommandHandler.execute()
    ↓
subprocess.run("ls -la", shell=True)
    ↓
Display output + capture for AI analysis
    ↓
Check exit code → success (0)
    ↓
Continue main loop
```

### Help Request Execution
```
User Input: "git?"
    ↓
main.py: get user input
    ↓
CommandRegistry.execute()
    ↓
Pattern match: ends with "?" → handle_help_request()
    ↓
OllamaHelper.get_help("git")
    ↓
_detect_context() → {is_git_repo: true, ...}
    ↓
_create_smart_prompt() → git-specific prompt
    ↓
Check cache → miss
    ↓
LoadingIndicator.start() → show spinner
    ↓
POST to Ollama API with prompt
    ↓
LoadingIndicator.stop() → hide spinner
    ↓
Cache response + display formatted help
    ↓
Continue main loop
```

### Error Handling Flow
```
User Input: "invalid_command"
    ↓
CommandHandler.execute()
    ↓
subprocess.run() → exit code 127 (command not found)
    ↓
CommandResult with stderr and exit_code
    ↓
main.py checks result.returncode != 0
    ↓
config.get('ai.help_on_error') → true
    ↓
OllamaHelper.get_error_help()
    ↓
AI analyzes error and suggests fixes
    ↓
Display AI suggestions
    ↓
Continue main loop
```

### Chat Mode Flow
```
User Input: "/chat"
    ↓
CommandRegistry.execute() → handle_chat()
    ↓
AppState.toggle_chat_mode() → chat_mode = True
    ↓
main.py loop: mode = "chat" if state.chat_mode else "normal"
    ↓
User Input in chat: "How do I find large files?"
    ↓
ChatHandler.handle_chat_input()
    ↓
Not a chat command → OllamaHelper.chat()
    ↓
Generate chat-optimized prompt
    ↓
POST to Ollama with longer response limit
    ↓
Display AI response
    ↓
Stay in chat mode (return True)
```

## Component Communication Patterns

### Dependency Injection
Components receive dependencies through constructor injection:
```python
# In main.py
config = Config()
ollama = OllamaHelper(config)  # Inject config
command_registry = CommandRegistry(ui, help_system, onboarding, ollama, config)
```

### Event Communication
While not formally implemented, communication happens through:
- **Method calls**: Direct component interaction
- **Return values**: Commands return success/failure status
- **State sharing**: AppState passed between components
- **Configuration**: Shared config object for behavior control

### Data Sharing Patterns
- **Configuration**: Global read-only access through Config object
- **State**: Mutable state through AppState object
- **Context**: Local context passed through method parameters
- **Results**: CommandResult objects for carrying execution data

## System Boundaries and Interfaces

### External System Interfaces
1. **Ollama API**: HTTP REST interface for AI operations
2. **Operating System**: subprocess interface for command execution
3. **File System**: Direct file I/O for config and history
4. **Terminal**: stdin/stdout for user interaction

### Internal Component Interfaces
1. **CommandRegistry ↔ Handlers**: Command routing protocol
2. **OllamaHelper ↔ Config**: Configuration access for AI settings
3. **UIUtils ↔ All Components**: Formatting service interface
4. **AppState ↔ Components**: Shared state modification protocol

## Security and Safety Model

### Command Execution Safety
- All commands executed through subprocess with shell=True
- No command filtering or blacklisting (preserves terminal freedom)
- Exit code monitoring for error detection
- Output capture prevents command injection through output

### AI Safety
- Local AI only (no external API calls by default)
- No sensitive data transmission
- Response validation and sanitization
- Timeout protection against hang scenarios

### Configuration Safety
- JSON validation on load
- Default value fallbacks for missing settings
- File permission checking
- Environment variable override protection

## Performance Characteristics

### Startup Performance
- **Cold start**: ~200-500ms (including Ollama health check)
- **Warm start**: ~100-200ms (if Ollama already running)
- **Memory footprint**: ~50-100MB base + AI model memory

### Runtime Performance
- **Command routing**: <1ms (hash map lookup)
- **System command execution**: Native subprocess performance
- **AI help generation**: 1-5 seconds (depending on model)
- **Cached AI responses**: <50ms

### Resource Usage
- **CPU**: Minimal when idle, moderate during AI operations
- **Memory**: Base ~50MB + AI model memory (2-8GB)
- **Network**: Local only (Ollama communication)
- **Disk**: Config files ~1KB, history ~100KB

## Error Handling Strategy

### Error Categories
1. **Configuration Errors**: Invalid JSON, missing files → use defaults
2. **AI Service Errors**: Ollama unavailable → graceful degradation
3. **Command Execution Errors**: Failed commands → offer AI help
4. **System Errors**: Python exceptions → log and continue

### Recovery Mechanisms
- **Graceful Degradation**: Core functionality works without AI
- **Default Fallbacks**: Built-in defaults for all configuration
- **Error Isolation**: Component failures don't crash the application
- **User Communication**: Clear error messages with suggested actions

## Extension Points

### Adding New Commands
1. Register command pattern in CommandRegistry
2. Implement handler method
3. Add configuration options if needed
4. Update help system

### Adding AI Providers
1. Implement provider interface (future)
2. Add provider configuration
3. Integrate with fallback system
4. Test with various scenarios

### Adding UI Components
1. Add methods to UIUtils class
2. Follow existing color conventions
3. Test terminal compatibility
4. Document usage patterns

This system overview provides the foundation for understanding TermSage's architecture and serves as a reference for development and extension activities.
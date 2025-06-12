# Project Architecture

## Overview
This document describes the technical architecture of TermSage, including system design, component relationships, and architectural decisions.

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
├── AI Docs/                 # AI context and documentation
│   ├── API_Summary.md       # External API documentation
│   ├── Coding_Conventions.md # Project standards
│   ├── Configuration_Guide.md # Configuration details
│   ├── Project_Architecture.md # This file
│   ├── Troubleshooting.md   # Common issues and solutions
│   └── User_Guide.md        # User documentation
├── Specs/                   # Feature specifications
│   └── Feature_Template.md  # Template for new features
├── .claude/                 # AI priming scripts
│   ├── prime.sh            # Shell script for context loading
│   └── prime.md            # Markdown prompt for AI tools
├── CLAUDE.md               # Quick reference guide
├── AI_DOCS.md              # AI memory and session notes
├── README.md               # User documentation
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project metadata
└── setup.py               # Package setup
```

## Architecture Principles

### 1. Layered Architecture
The system follows a clean layered architecture:

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│    (Terminal UI, User Interaction)      │
├─────────────────────────────────────────┤
│         Business Logic Layer            │
│  (Command Processing, AI Integration)   │
├─────────────────────────────────────────┤
│           Data Layer                    │
│  (Config, History, State Management)    │
└─────────────────────────────────────────┘
```

### 2. Component Architecture

#### Core Components

**Terminal Interface (`main.py`)**
- Handles user input/output
- Manages terminal session lifecycle
- Implements readline for command history
- Coordinates between components

**Command Handler (`command_handler.py`)**
- Validates and sanitizes commands
- Executes system commands via subprocess
- Implements safety checks
- Handles command failures

**Configuration Manager (`config.py`)**
- Loads and validates configuration
- Manages runtime settings
- Handles provider switching
- Stores user preferences

**AI Integration (future: `ai/`)**
- Abstracts different AI providers
- Manages model selection
- Handles context management
- Implements fallback strategies

### 3. Data Flow

```
User Input → Terminal Interface → Command Handler
                ↓                       ↓
           AI Enhancement         Command Execution
                ↓                       ↓
           AI Response            System Response
                ↓                       ↓
            Terminal Output ← Result Processor
```

### 4. Key Design Patterns

#### Strategy Pattern
Used for AI provider selection:
```python
class AIProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass

class OllamaProvider(AIProvider):
    def complete(self, prompt: str) -> str:
        # Ollama-specific implementation
        pass

class OpenAIProvider(AIProvider):
    def complete(self, prompt: str) -> str:
        # OpenAI-specific implementation
        pass
```

#### Command Pattern
For command execution:
```python
class Command:
    def __init__(self, cmd_str: str):
        self.cmd_str = cmd_str
        self.result = None
    
    def execute(self) -> CommandResult:
        # Validation and execution logic
        pass
```

#### Observer Pattern
For event handling:
```python
class EventEmitter:
    def __init__(self):
        self._observers = {}
    
    def on(self, event: str, callback: Callable):
        # Register observer
        pass
    
    def emit(self, event: str, data: Any):
        # Notify observers
        pass
```

## Technical Architecture

### 1. Command Execution Pipeline
```
1. User Input
2. Input Parsing & Tokenization
3. Safety Validation
4. Command Execution (subprocess)
5. Result Processing
6. AI Enhancement (if needed)
7. Output Formatting
8. Display to User
```

### 2. AI Integration Points
- **Pre-execution**: Command suggestions and validation
- **Post-execution**: Error analysis and troubleshooting
- **Interactive**: Chat mode for discussions
- **Background**: Auto-completion enhancement

### 3. Async Architecture
```python
# AI operations are non-blocking
async def enhance_command(cmd: str) -> str:
    # Get AI suggestions without blocking terminal
    suggestion = await ai_provider.suggest(cmd)
    return suggestion

# Terminal remains responsive
def terminal_loop():
    while True:
        user_input = get_input()
        
        # Execute immediately
        result = execute_command(user_input)
        
        # Enhance asynchronously if needed
        if needs_ai_help(result):
            asyncio.create_task(get_ai_help(result))
```

### 4. Memory Management
- **Command History**: Limited circular buffer
- **AI Context**: Sliding window with importance scoring
- **Session State**: Lightweight state machine
- **Cache**: LRU cache for AI responses

### 5. Security Architecture
```
Input → Sanitization → Validation → Whitelist Check → Execution
                           ↓
                    Blacklist Check
                           ↓
                    Permission Check
```

## Module Responsibilities

### `main.py`
- Initialize terminal environment
- Setup readline and history
- Main event loop
- Coordinate components
- Handle graceful shutdown

### `command_handler.py`
- Parse command strings
- Validate command safety
- Execute via subprocess
- Capture and process output
- Handle timeouts and errors

### `config.py`
- Load configuration files
- Validate settings
- Provide configuration API
- Handle dynamic updates
- Manage defaults

### Future Modules

#### `ai/providers.py`
- Abstract base for AI providers
- Implement specific providers
- Handle authentication
- Manage rate limits

#### `ai/context.py`
- Manage conversation context
- Implement context windowing
- Score message importance
- Handle context persistence

#### `ui/autocomplete.py`
- Implement tab completion
- Integrate AI suggestions
- Manage completion history
- Handle fuzzy matching

## Performance Considerations

### 1. Response Time Targets
- Command execution: < 50ms overhead
- Tab completion: < 100ms
- AI suggestions: < 500ms (async)
- Terminal startup: < 200ms

### 2. Resource Limits
- Memory usage: < 100MB baseline
- CPU usage: < 5% idle
- AI context: 10k tokens max
- History: 10k commands

### 3. Optimization Strategies
- Lazy loading of AI providers
- Command result caching
- Precompiled regex patterns
- Efficient subprocess usage

## Scalability Design

### 1. Horizontal Scaling
- Stateless command execution
- Distributable AI requests
- Shared configuration store
- Session state in Redis (future)

### 2. Vertical Scaling
- Configurable resource limits
- Adjustable context windows
- Model size selection
- Performance tier settings

## Future Architecture Enhancements

### 1. Plugin System
```python
class Plugin(ABC):
    @abstractmethod
    def on_command(self, cmd: Command) -> None:
        pass
    
    @abstractmethod
    def on_result(self, result: CommandResult) -> None:
        pass
```

### 2. Remote Execution
- SSH integration
- Container support
- Cloud shell compatibility
- Distributed commands

### 3. Advanced AI Features
- Multi-model ensemble
- Fine-tuned models
- Local model training
- Personalization engine

## Architecture Decision Records (ADRs)

### ADR-001: Use Python as Primary Language
**Status**: Accepted
**Context**: Need cross-platform support with good library ecosystem
**Decision**: Use Python 3.8+ for implementation
**Consequences**: Good library support, slower than compiled languages

### ADR-002: Subprocess for Command Execution
**Status**: Accepted
**Context**: Need reliable command execution with proper isolation
**Decision**: Use subprocess module with careful configuration
**Consequences**: Clean separation, some overhead for process creation

### ADR-003: Multiple AI Provider Support
**Status**: Accepted
**Context**: Users need flexibility in AI provider choice
**Decision**: Abstract provider interface with multiple implementations
**Consequences**: More complex but flexible, need good abstraction

### ADR-004: Async AI Operations
**Status**: Accepted
**Context**: AI calls shouldn't block terminal responsiveness
**Decision**: Use asyncio for all AI operations
**Consequences**: More complex code, better user experience
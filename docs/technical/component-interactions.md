# Component Interactions and Communication

## Overview
This document details how TermSage components interact with each other, the communication patterns used, and the data flows between different parts of the system. Understanding these interactions is crucial for debugging issues and extending functionality.

## Component Relationship Diagram

```
                                   ┌─────────────┐
                                   │   main.py   │
                                   │ (Orchestrator)│
                                   └──────┬──────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
            ┌───────▼───────┐    ┌────────▼────────┐    ┌──────▼──────┐
            │ CommandRegistry│    │   UIUtils       │    │   Config    │
            │  (Router)      │    │ (Formatter)     │    │ (Settings)  │
            └───────┬───────┘    └─────────────────┘    └─────────────┘
                    │                     ▲                     ▲
          ┌─────────┼─────────┐          │                     │
          │         │         │          │                     │
    ┌─────▼─────┐ ┌─▼──────┐ ┌▼────────▼─┐                    │
    │CommandHdlr│ │OllamaHlp│ │HelpSystem │                    │
    │(Executor) │ │(AI Integ)│ │(Tutorial) │                    │
    └───────────┘ └────┬────┘ └───────────┘                    │
                       │                                       │
                    ┌──▼──────────────────────────────────────▼┐
                    │              AppState                     │
                    │           (Session Data)                  │
                    └───────────────────────────────────────────┘
```

## Detailed Component Interactions

### 1. Application Bootstrap (main.py)

**Initialization Sequence**:
```python
def main():
    # 1. Load configuration first (everything depends on this)
    config = Config()
    
    # 2. Initialize core services
    command_handler = CommandHandler()
    ollama = OllamaHelper(config)  # Needs config for URL/model
    ui = UIUtils()
    
    # 3. Initialize higher-level services
    help_system = HelpSystem(config, ollama)  # Needs both config and AI
    onboarding = OnboardingWizard(config)
    
    # 4. Create state management
    state = AppState()
    
    # 5. Initialize command routing (needs everything)
    command_registry = CommandRegistry(ui, help_system, onboarding, ollama, config)
    command_registry.set_state(state)  # Inject state after creation
    
    # 6. Create specialized handlers
    chat_handler = ChatHandler(ui, ollama, state)
```

**Dependency Flow**:
- `Config` → Created first, no dependencies
- `CommandHandler` → Standalone, no dependencies  
- `OllamaHelper` → Depends on `Config`
- `UIUtils` → Standalone, no dependencies
- `HelpSystem` → Depends on `Config` and `OllamaHelper`
- `AppState` → Standalone, no dependencies
- `CommandRegistry` → Depends on all other components
- `ChatHandler` → Depends on `UIUtils`, `OllamaHelper`, `AppState`

### 2. Command Processing Flow

**Normal Command Path**:
```
User Input: "ls -la"
│
▼
main.py: input(get_prompt(ui, mode))
│
▼ 
state.add_command(user_input)  # Track for contextual help
│
▼
command_registry.execute(user_input)
│
├─ Check built-in commands → None (not found)
│
▼
command_handler.execute(user_input)
│
├─ subprocess.run("ls -la", shell=True, capture_output=True)
├─ Print output immediately
├─ Return CommandResult(stdout, stderr, exit_code)
│
▼
if cmd_result.returncode != 0:
    ├─ config.get('ai.help_on_error') → true
    ├─ ollama.get_error_help(command, stderr)
    └─ ui.ai_response(error_help) → print formatted suggestion
```

**Help Request Path**:
```
User Input: "git?"
│
▼
command_registry.execute("git?")
│
├─ Check exact matches → None
├─ Check pattern matches → None  
├─ Check help pattern → Match!
│
▼
handle_help_request("git?")
│
├─ command_name = "git" (strip ?)
├─ ollama.is_help_cached("git") → false
│
▼
LoadingIndicator("Getting help", ui)
├─ indicator.start() → spawn animation thread
│
▼
ollama.get_help("git")
│
├─ _detect_context() → {is_git_repo: true, ...}
├─ _create_smart_prompt("git", context)
├─ requests.post(ollama_url, prompt_data)
├─ Cache response in self._help_cache
│
▼
indicator.stop() → clear animation
print(ui.ai_response(help_text))
```

**Chat Mode Path**:
```
User Input: "/chat"
│
▼
command_registry.execute("/chat")
│
├─ Check exact matches → Found: handle_chat()
│
▼
handle_chat()
│
├─ state.toggle_chat_mode() → chat_mode = True
├─ print(ui.info("Entered chat mode"))
│
▼
Main loop continues with chat_mode = True
│
User Input: "How do I find large files?"
│
▼
chat_handler.handle_chat_input("How do I find large files?")
│
├─ Check chat commands → None
├─ ollama.chat(user_input)
│   ├─ Create chat prompt
│   ├─ POST to Ollama with chat options
│   └─ Return AI response
├─ print(ui.ai_response(response))
└─ return True (stay in chat mode)
```

### 3. Configuration System Interactions

**Configuration Loading**:
```python
# Config.__init__()
config_path = PathManager.get_config_file()  # ~/.termsage/config.json
│
├─ File exists?
│   ├─ Yes: Load JSON + merge with defaults
│   └─ No: Create with defaults
│
├─ Validate and save if modified
└─ Store in self.settings
```

**Configuration Access Patterns**:
```python
# Components access config through dependency injection
class OllamaHelper:
    def __init__(self, config):
        self.config = config
        self.base_url = config.get_ollama_url()      # "ai.base_url"
        self.current_model = config.get_ollama_model()  # "ai.model"

# Dot notation access
config.get('ai.model', 'llama2')           # Get with default
config.set('ai.model', 'codellama')        # Set nested value
config.save()                              # Persist to disk
```

**Configuration Update Flow**:
```
User: "/model codellama"
│
▼
command_registry.handle_model_switch("/model codellama")
│
├─ model_name = "codellama"
├─ ollama.is_available() → check Ollama status
├─ ollama.switch_model("codellama")
│   ├─ Validate model exists
│   ├─ self.current_model = "codellama"
│   ├─ config.set_ollama_model("codellama")
│   │   ├─ config.set('ai.model', 'codellama')
│   │   └─ config.save()  # Write to disk
│   └─ print("✓ Switched to model: codellama")
```

### 4. AI Integration Communication

**OllamaHelper Service Interface**:
```python
class OllamaHelper:
    # Health and availability
    def is_available(self) -> bool              # Quick health check
    def test_model(self) -> bool                # Test current model
    
    # Help and assistance  
    def get_help(self, command: str) -> str     # Context-aware help
    def chat(self, message: str) -> str         # Interactive chat
    def get_error_help(self, cmd, error) -> str # Error analysis
    
    # Model management
    def list_models(self) -> None               # Display available models
    def switch_model(self, name: str) -> bool   # Change active model
    def get_model_info(self) -> Dict            # Current model details
```

**Context Detection Integration**:
```python
# OllamaHelper._detect_context()
def _detect_context(self) -> dict:
    return {
        'is_git_repo': os.path.exists('.git'),
        'is_node_project': os.path.exists('package.json'),
        'is_python_project': os.path.exists('requirements.txt') or 
                           os.path.exists('pyproject.toml'),
        'is_docker_project': os.path.exists('Dockerfile'),
        'current_dir': os.path.basename(os.getcwd())
    }

# Usage in help generation
context = self._detect_context()
if context['is_git_repo']:
    prompt = f"Git help for: {command}\nContext: In git repository\n..."
```

**Caching System**:
```python
# Response caching for performance
def get_help(self, command: str) -> str:
    cache_key = f"help_{command}_{os.getcwd()}"
    
    # Check cache first
    if hasattr(self, '_help_cache') and cache_key in self._help_cache:
        return self._help_cache[cache_key]
    
    # Generate new response
    response = self._generate_help(command)
    
    # Cache the response
    if not hasattr(self, '_help_cache'):
        self._help_cache = {}
    self._help_cache[cache_key] = response
    
    # Maintain cache size
    if len(self._help_cache) > 20:
        self._help_cache.pop(next(iter(self._help_cache)))
    
    return response
```

### 5. State Management Communication

**AppState Integration Points**:
```python
class AppState:
    def __init__(self):
        self.chat_mode = False           # Current mode
        self.recent_commands = []        # For contextual tips
        self.command_count = 0          # For tip frequency
    
    def add_command(self, command: str):
        """Called by main loop for every command"""
        self.recent_commands.append(command)
        if len(self.recent_commands) > 50:
            self.recent_commands.pop(0)
        self.command_count += 1
    
    def get_recent_commands(self, limit: int = 10) -> list:
        """Used by help system for contextual tips"""
        return self.recent_commands[-limit:]
```

**State Usage Patterns**:
```python
# Main loop uses state for mode detection
mode = "chat" if state.chat_mode else "normal"
prompt = get_prompt(ui, mode)

# Help system uses state for contextual tips  
if state.command_count > 0 and state.command_count % 10 == 0:
    tips = help_system.get_contextual_tips(os.getcwd(), state.get_recent_commands())
    for tip in tips:
        print(tip)

# Command registry uses state for mode switching
def handle_chat(self) -> bool:
    if self.state:
        self.state.toggle_chat_mode()
        print(self.ui.info("Entered chat mode"))
```

### 6. UI System Communication

**UIUtils Service Interface**:
```python
class UIUtils:
    # Message formatting
    def success(self, text: str) -> str    # ✓ Green message
    def error(self, text: str) -> str      # ✗ Red message  
    def warning(self, text: str) -> str    # ⚠ Yellow message
    def info(self, text: str) -> str       # ℹ Blue message
    def ai_response(self, text: str) -> str # 🤖 Cyan message
    
    # Special formatting
    def command(self, text: str) -> str    # Bold command text
    def prompt(self, text: str) -> str     # Magenta prompt
    def dim(self, text: str) -> str        # Dimmed text
    
    # Color support
    def colorize(self, text, color, bold=False) -> str
```

**Loading Indicator Integration**:
```python
# Used by AI operations
indicator = LoadingIndicator("Getting help", ui)
indicator.start()  # Spawns animation thread

try:
    result = ollama.get_help(command)
finally:
    indicator.stop()  # Cleans up animation
```

**Component UI Usage**:
```python
# CommandRegistry uses UI for all output
print(self.ui.success("Goodbye!"))          # Exit message
print(self.ui.error("Usage: /model <name>")) # Error message
print(self.ui.ai_response(help_text))        # AI help display

# OllamaHelper uses UI for status messages  
print(self.ui.warning("Ollama not available"))
print(self.ui.success(f"✓ Switched to model: {model_name}"))

# Main loop uses UI for prompts
prompt = get_prompt(ui, mode)  # Formatted directory prompt
```

### 7. Error Handling and Communication

**Error Propagation Patterns**:
```python
# Component-level error handling
class OllamaHelper:
    def get_help(self, command: str) -> str:
        try:
            response = self._make_request("generate", "POST", data)
            return self._format_response(response)
        except requests.Timeout:
            return f"⏱️ Response timeout. Try: man {command}"
        except requests.RequestException:
            return f"❌ Connection error. Try: man {command}"
        except Exception as e:
            return f"❌ Error getting help: {e}"

# Application-level error handling
def main():
    while True:
        try:
            # Command processing...
        except KeyboardInterrupt:
            print("\n" + ui.dim("^C"))
            if state.chat_mode:
                state.chat_mode = False
                print(ui.info("Exited chat mode"))
            continue
        except EOFError:
            print("\n" + ui.success("Goodbye!"))
            break
        except Exception as e:
            print(ui.error(f"Unexpected error: {e}"))
            continue
```

**Error Recovery Communication**:
```python
# Command execution error handling
cmd_result = command_handler.execute(user_input)
if cmd_result and cmd_result.returncode != 0:
    # Failed command - offer AI help
    if config.get('ai.help_on_error', True) and ollama.is_available():
        print(ui.info("Command failed. Getting AI suggestions..."))
        try:
            error_help = ollama.get_error_help(user_input, cmd_result.stderr)
            print(ui.ai_response(error_help))
        except:
            pass  # Graceful degradation
```

## Data Flow Patterns

### 1. Synchronous Data Flow
Most component communication is synchronous and direct:
```python
config → ollama_helper.base_url
user_input → command_registry → command_handler → subprocess
ai_response → ui_utils.format → terminal_output
```

### 2. Asynchronous Operations
Limited async operations (simulated with threads):
```python
# Loading indicators use background threads
LoadingIndicator.start() → Thread(target=self._animate)
AI API call (blocking)
LoadingIndicator.stop() → Join thread + cleanup
```

### 3. Event-Driven Patterns
Implicit event handling through method calls:
```python
# "Events" are method calls with specific return values
command_registry.execute() → True (continue) | False (exit) | None (not handled)
chat_handler.handle_chat_input() → True (stay in chat) | False (exit chat)
```

## Communication Protocols

### 1. Return Value Protocols
```python
# CommandRegistry.execute() protocol
True  → Command handled, continue main loop
False → Command handled, exit application  
None  → Command not handled, try next handler

# AI Helper protocols
str   → Success, return response text
""    → Empty response (handled gracefully)
"❌..." → Error message (formatted for user display)
```

### 2. Exception Handling Protocols
```python
# Network operations (Ollama API)
requests.Timeout     → Show timeout message
requests.RequestException → Show connection error
JSON decode error    → Show parsing error

# File operations (Config)
FileNotFoundError    → Create with defaults
PermissionError      → Show permission message
JSON decode error    → Use defaults, warn user
```

### 3. Configuration Protocols
```python
# All components follow this pattern for config access
def __init__(self, config):
    self.config = config
    self.setting = config.get('section.setting', default_value)

# Config updates always go through config object
config.set('section.setting', new_value)
config.save()  # Persist to disk
```

## Threading and Concurrency

### Current Threading Model
TermSage uses minimal threading:
- **Main thread**: UI and command processing (blocking)
- **Animation threads**: Loading indicators (background, daemon)
- **No worker threads**: All AI operations are blocking

### Thread Safety Considerations
```python
# LoadingIndicator thread safety
class LoadingIndicator:
    def __init__(self):
        self.is_running = False  # Shared flag
        self.thread = None
    
    def start(self):
        if self.is_running:  # Prevent double-start
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True  # Dies with main thread
        self.thread.start()
    
    def stop(self):
        self.is_running = False  # Signal stop
        if self.thread:
            self.thread.join()     # Wait for cleanup
```

### Future Concurrency Considerations
For async AI operations:
```python
# Potential future pattern
async def get_help_async(self, command: str) -> str:
    # Non-blocking AI request
    response = await self.ai_client.generate(prompt)
    return response

# Main loop integration
async def main_loop():
    while True:
        user_input = await async_input()
        if user_input.endswith('?'):
            # Start AI request in background
            help_task = asyncio.create_task(get_help_async(command))
            # Continue with other work...
            result = await help_task
```

## Component Extension Points

### Adding New Components
1. **Follow dependency injection pattern**:
   ```python
   class NewComponent:
       def __init__(self, config, ui, other_deps):
           self.config = config
           self.ui = ui
   ```

2. **Register with main orchestrator**:
   ```python
   # In main.py
   new_component = NewComponent(config, ui, ollama)
   command_registry.add_component(new_component)
   ```

3. **Follow communication protocols**:
   - Use UIUtils for all output formatting
   - Access config through dependency injection
   - Return appropriate status codes
   - Handle errors gracefully

### Extending Existing Components
1. **CommandRegistry**: Add new command patterns
2. **OllamaHelper**: Add new AI operation types
3. **UIUtils**: Add new formatting functions
4. **Config**: Add new configuration sections
5. **AppState**: Add new state variables

This detailed understanding of component interactions enables effective debugging, testing, and extension of the TermSage system.
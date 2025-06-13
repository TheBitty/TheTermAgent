# Nvim-Like Commands and Enhanced UI Design

## Overview
This document outlines a design for implementing vim/nvim-like commands and a multi-window interface to enhance the TermSage user experience beyond traditional terminal limitations.

## Core Problems to Solve

### 1. Command Editing Limitations
- **Current Issue**: Basic readline editing, no visual feedback
- **Solution**: Modal editing with vim-like keybindings
- **Benefits**: Familiar interface for developers, powerful editing capabilities

### 2. Single Context Limitation  
- **Current Issue**: Everything happens in one terminal window
- **Solution**: Multi-window/tab interface with specialized panes
- **Benefits**: Parallel workflows, dedicated AI interaction space

### 3. AI Integration Friction
- **Current Issue**: AI responses mixed with command output
- **Solution**: Dedicated AI window with persistent context
- **Benefits**: Cleaner separation, better conversation tracking

## Proposed Architecture

### Modal System Design

#### Command Mode (Default)
```
TermSage [Normal] ~/project $ _
```
- Default state, ready for command input
- Vim-like navigation: `h`, `j`, `k`, `l` for cursor movement
- Quick commands: `:` for command palette, `/` for search

#### Edit Mode (Command Editing)
```
TermSage [Edit] ~/project $ git commit -m "fix: update config_
```
- Enter with `i`, `a`, `o` (insert, append, new line)
- Full vim editing capabilities
- Syntax highlighting for commands
- Auto-completion with `Tab`

#### Visual Mode (Selection)
```
TermSage [Visual] ~/project $ git [commit -m "fix: update] config
```
- Enter with `v` for character selection, `V` for line selection
- Copy/paste with `y`/`p`
- Quick operations on selected text

#### Command Palette Mode
```
TermSage [Command] :help git
```
- Enter with `:`
- Access to all TermSage commands
- History search and execution
- AI query interface

### Multi-Window Interface

#### Main Terminal Window
```
┌─ TermSage Main ─────────────────────────────────────┐
│ ~/project $ git status                              │
│ On branch main                                      │
│ Your branch is up to date with 'origin/main'.      │
│                                                     │
│ Changes to be committed:                            │
│   (use "git restore --staged <file>..." to unstage)│
│         modified:   src/main.py                     │
│                                                     │
│ TermSage [Normal] ~/project $ _                     │
└─────────────────────────────────────────────────────┘
```

#### Dedicated AI Window
```
┌─ AI Assistant ──────────────────────────────────────┐
│ 🤖 How can I help you?                             │
│                                                     │
│ 💬 You: How do I undo the last git commit?         │
│                                                     │
│ 🤖 AI: To undo the last git commit, you have       │
│ several options:                                    │
│                                                     │
│ 1. Keep changes (soft reset):                      │
│    git reset --soft HEAD~1                         │
│                                                     │
│ 2. Discard changes (hard reset):                   │
│    git reset --hard HEAD~1                         │
│                                                     │
│ 💬 Ask AI: _                                       │
└─────────────────────────────────────────────────────┘
```

#### Command History/Buffer List
```
┌─ History ───────────────────────────────────────────┐
│ 1  git status                                       │
│ 2  ls -la                                          │
│ 3  cd src/                                         │
│ 4  vim main.py                                     │
│ 5  git add .                                       │
│ 6  git commit -m "fix: update config"             │
│                                                     │
│ [Press Enter to execute, 'e' to edit]              │
└─────────────────────────────────────────────────────┘
```

## Vim-Like Command System

### Navigation Commands
```
h, j, k, l          - Move cursor left, down, up, right
w, b                - Move word forward/backward  
0, $                - Move to beginning/end of line
gg, G               - Move to first/last command in history
Ctrl+u, Ctrl+d     - Scroll up/down through output
```

### Editing Commands
```
i                   - Insert mode at cursor
a                   - Insert mode after cursor
A                   - Insert mode at end of line
o                   - New line below and insert
O                   - New line above and insert
x                   - Delete character
dd                  - Delete entire command
yy                  - Copy command
p                   - Paste after cursor
u                   - Undo last change
Ctrl+r              - Redo
```

### Command Mode Operations
```
:q                  - Quit TermSage
:w                  - Save command to history
:e <file>           - Edit file
:split              - Split window horizontally  
:vsplit             - Split window vertically
:ai <query>         - Query AI in dedicated window
:history            - Show command history window
:tabs               - Show all open tabs
```

### Window Management
```
Ctrl+w h/j/k/l      - Navigate between windows
Ctrl+w s            - Split horizontally
Ctrl+w v            - Split vertically  
Ctrl+w c            - Close current window
Ctrl+w o            - Close all but current window
Ctrl+t              - New tab
gt, gT              - Next/previous tab
```

## Enhanced Features

### 1. Smart Command Completion
```
git co<Tab>         → git commit, git checkout, git config
docker r<Tab>       → docker run, docker restart, docker rm
npm i<Tab>          → npm install, npm init
```

### 2. Syntax Highlighting
```bash
git commit -m "fix: update config"
│   │      │  └─ String (green)
│   │      └─ Flag (blue)  
│   └─ Subcommand (yellow)
└─ Command (cyan)
```

### 3. AI Integration Modes

#### Inline AI Suggestions
```
~/project $ git commit -m "
                         └─ 💡 AI suggests: "fix: resolve configuration issue"
```

#### Command Explanation
```
~/project $ docker run -it --rm ubuntu bash?
┌─ AI Explanation ────────────────────────────────────┐
│ This command:                                       │
│ • Runs Ubuntu container interactively (-it)        │
│ • Removes container after exit (--rm)              │  
│ • Starts bash shell                                 │
└─────────────────────────────────────────────────────┘
```

#### Error Analysis Window
```
┌─ Error Analysis ────────────────────────────────────┐
│ Command failed: npm install                         │
│ Exit code: 1                                        │
│                                                     │
│ 🤖 AI Analysis:                                     │
│ The error suggests missing package.json. Try:      │
│                                                     │
│ 1. npm init (to create package.json)               │
│ 2. Check if you're in the right directory          │
│ 3. Verify npm is properly installed                │
│                                                     │
│ [Press 'f' to fix automatically]                   │
└─────────────────────────────────────────────────────┘
```

## Implementation Strategy

### Phase 1: Modal Interface
1. Implement basic modal system (Normal/Insert/Command modes)
2. Add vim-like key bindings for navigation and editing
3. Create command palette with `:` prefix
4. Basic window management

### Phase 2: Multi-Window System  
1. Terminal multiplexer integration (tmux-like)
2. Window splitting and tabbing
3. Dedicated AI pane
4. History and buffer management

### Phase 3: Advanced Features
1. Syntax highlighting engine
2. Smart completion system
3. AI integration improvements
4. Custom key binding configuration

### Phase 4: Extensibility
1. Plugin system for custom commands
2. Theme support
3. Configuration management
4. Performance optimizations

## Technical Considerations

### Dependencies
```python
# Core terminal handling
import curses          # For advanced terminal control
import ncurses         # Alternative terminal library

# Terminal multiplexing
import pexpect         # For process management
import ptyprocess      # For pseudo-terminal handling

# UI Components  
import rich            # For styling and layout
import textual         # For TUI framework
import blessed         # For terminal formatting

# Vim-like functionality
import prompt_toolkit  # For advanced input handling
import pygments        # For syntax highlighting
```

### Architecture Components

#### 1. Modal Controller
```python
class ModalController:
    def __init__(self):
        self.current_mode = Mode.NORMAL
        self.key_handlers = {
            Mode.NORMAL: NormalModeHandler(),
            Mode.INSERT: InsertModeHandler(), 
            Mode.VISUAL: VisualModeHandler(),
            Mode.COMMAND: CommandModeHandler()
        }
    
    def handle_key(self, key):
        return self.key_handlers[self.current_mode].handle(key)
```

#### 2. Window Manager
```python
class WindowManager:
    def __init__(self):
        self.windows = []
        self.active_window = None
        self.layout = Layout()
    
    def split_window(self, direction):
        # Implementation for window splitting
        pass
    
    def switch_window(self, direction):
        # Implementation for window navigation
        pass
```

#### 3. AI Integration Layer
```python
class AIIntegrationLayer:
    def __init__(self):
        self.ai_window = AIWindow()  
        self.context_manager = ContextManager()
    
    def handle_ai_query(self, query):
        # Route to dedicated AI window
        pass
    
    def provide_inline_suggestion(self, command):
        # Show suggestions in main terminal
        pass
```

## User Experience Improvements

### 1. Seamless Editing
- No more awkward backspacing through long commands
- Visual feedback for all edits
- Multi-line command support
- Persistent edit history

### 2. Parallel Workflows
- Run commands while chatting with AI
- Keep reference information visible
- Multiple terminal sessions in tabs
- Context doesn't get mixed up

### 3. Enhanced AI Interaction
- Dedicated space for AI conversations
- Persistent chat history
- Contextual help without cluttering main terminal
- AI can reference visible command output

### 4. Power User Features
- Macros and custom key bindings
- Command templates and snippets
- Advanced search and filtering
- Scriptable automation

## Migration Path

### Backward Compatibility
- Traditional terminal mode always available
- Gradual feature introduction
- User can disable modal features
- Existing commands work unchanged

### Learning Curve
- Built-in tutorial for vim-like features
- Progressive disclosure of advanced features
- Contextual help system
- Familiar fallbacks for new users

## Future Enhancements

### IDE-Like Features
- File explorer pane
- Integrated text editing
- Project management
- Version control visualization

### Advanced AI Features
- Code generation in dedicated pane
- Real-time command suggestions
- Automated error fixing
- Learning from user patterns

### Collaboration Features
- Shared terminal sessions
- Command sharing and templates
- Team AI contexts
- Remote pair programming support
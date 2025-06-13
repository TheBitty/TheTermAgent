# AI Window Integration Design

## Overview
This document outlines the design for a dedicated AI interaction window that provides a superior user experience compared to the current mixed-context chat mode, enabling persistent AI conversations alongside terminal operations.

## Current AI Integration Issues

### Problems with Current `/chat` Mode
1. **Context Pollution**: AI responses mixed with command output
2. **Lost History**: Terminal commands scroll AI conversations out of view  
3. **Mode Switching**: Constant toggling between `/chat` and normal mode
4. **No Persistence**: AI context lost when exiting chat mode
5. **Single Focus**: Can't use AI while running commands

### Current User Flow (Problematic)
```
$ git status
On branch main...

$ /chat
[Chat] $ How do I fix merge conflicts?
🤖 AI: Here are the steps to resolve merge conflicts...

[Chat] $ /exit
$ git merge feature-branch
CONFLICT (content): Merge conflict in src/main.py
Auto-merge failed; fix conflicts and commit the result.

$ /chat  # Lost previous AI context!
[Chat] $ The merge failed, what do I do?
🤖 AI: I don't have context about your previous merge...
```

## Proposed AI Window Solution

### Seamless Parallel Workflow
```
┌─ Terminal ──────────────────┬─ AI Assistant ─────────────────┐
│ $ git status               │ 🤖 How can I help you?        │
│ On branch main             │                                │
│ Your branch is ahead...    │ 💬 You: How do I fix merge     │
│                            │ conflicts?                     │
│ $ git merge feature-branch │                                │
│ CONFLICT: Merge conflict   │ 🤖 AI: Here are the steps:    │
│ in src/main.py            │                                │
│                            │ 1. Open the conflicted file   │
│ $ vim src/main.py         │ 2. Look for <<<<<<< markers   │
│ [Opens in editor]          │ 3. Choose which changes...     │
│                            │                                │
│ $ git add src/main.py     │ 💬 You: I fixed the conflicts │
│ $ git commit              │                                │
│                            │ 🤖 AI: Great! The merge is    │
│ $ _                       │ now complete. You can push...  │
│                            │                                │
│                            │ 💬 Ask: _                     │
└────────────────────────────┴────────────────────────────────┘
```

## AI Window Architecture

### 1. Persistent AI Context Manager

#### Context Preservation
```python
class AIContextManager:
    """Manages persistent AI conversation context"""
    
    def __init__(self):
        self.conversation_history: List[Message] = []
        self.terminal_context: TerminalContext = TerminalContext()
        self.project_context: ProjectContext = ProjectContext()
        self.session_metadata: Dict = {}
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add message to conversation history"""
        
    def get_context_summary(self) -> str:
        """Generate summary of current context for AI"""
        
    def update_terminal_context(self, command: str, output: str, exit_code: int):
        """Update context with terminal activity"""
        
    def save_conversation(self, session_id: str):
        """Save conversation for later restoration"""
        
    def load_conversation(self, session_id: str):
        """Load previous conversation"""
```

#### Context Types
```python
class TerminalContext:
    """Terminal-specific context information"""
    
    def __init__(self):
        self.current_directory: str = os.getcwd()
        self.recent_commands: List[Command] = []
        self.last_command_output: str = ""
        self.last_exit_code: int = 0
        self.environment_vars: Dict[str, str] = {}
        self.running_processes: List[Process] = []

class ProjectContext:
    """Project-level context information"""
    
    def __init__(self):
        self.project_type: str = ""  # git, node, python, etc.
        self.key_files: List[str] = []
        self.dependencies: List[str] = []
        self.recent_changes: List[FileChange] = []
        self.git_status: GitStatus = None
```

### 2. Intelligent Context Awareness

#### Automatic Context Updates
```python
class ContextAwareness:
    """Automatically updates AI context based on terminal activity"""
    
    def __init__(self, ai_context: AIContextManager):
        self.ai_context = ai_context
        self.context_rules = self._load_context_rules()
    
    def on_command_executed(self, command: str, output: str, exit_code: int):
        """Update AI context when terminal command is executed"""
        
        # Parse command for context clues
        if command.startswith('cd '):
            self._update_directory_context(command, output)
        elif command.startswith('git '):
            self._update_git_context(command, output, exit_code)
        elif command.startswith('npm ') or command.startswith('pip '):
            self._update_dependency_context(command, output)
        elif exit_code != 0:
            self._update_error_context(command, output, exit_code)
    
    def _update_git_context(self, command: str, output: str, exit_code: int):
        """Update git-specific context"""
        if 'git status' in command:
            self.ai_context.project_context.git_status = self._parse_git_status(output)
        elif 'git log' in command:
            self.ai_context.project_context.recent_commits = self._parse_git_log(output)
```

#### Smart Context Injection
```python
def generate_ai_prompt(self, user_query: str, context: AIContextManager) -> str:
    """Generate enhanced prompt with relevant context"""
    
    base_prompt = f"User question: {user_query}\n\n"
    
    # Add terminal context if relevant
    if self._is_terminal_related(user_query):
        base_prompt += f"Current directory: {context.terminal_context.current_directory}\n"
        base_prompt += f"Last command: {context.terminal_context.recent_commands[-1]}\n"
        
        if context.terminal_context.last_exit_code != 0:
            base_prompt += f"Last command failed with exit code: {context.terminal_context.last_exit_code}\n"
            base_prompt += f"Error output: {context.terminal_context.last_command_output}\n"
    
    # Add project context if relevant  
    if self._is_project_related(user_query):
        base_prompt += f"Project type: {context.project_context.project_type}\n"
        if context.project_context.git_status:
            base_prompt += f"Git status: {context.project_context.git_status.summary}\n"
    
    return base_prompt
```

### 3. Enhanced AI Window Interface

#### Interactive Response Features
```python
class AIResponseRenderer:
    """Renders AI responses with interactive elements"""
    
    def render_response(self, response: str, metadata: Dict = None) -> RenderedResponse:
        """Render AI response with interactive elements"""
        
        rendered = RenderedResponse()
        
        # Parse code blocks and make them executable
        code_blocks = self._extract_code_blocks(response)
        for block in code_blocks:
            if block.language in ['bash', 'sh', 'zsh']:
                rendered.add_executable_code(block.content)
        
        # Parse file references and make them clickable
        file_refs = self._extract_file_references(response)
        for file_ref in file_refs:
            rendered.add_file_link(file_ref.path, file_ref.line_number)
        
        # Add action buttons
        rendered.add_action_button("Copy to Clipboard", lambda: self._copy_response(response))
        rendered.add_action_button("Send to Terminal", lambda: self._send_to_terminal(response))
        rendered.add_action_button("Save as Snippet", lambda: self._save_snippet(response))
        
        return rendered
```

#### AI Window Layout Components
```
┌─ AI Assistant ──────────────────────────────────────────────┐
│ 🔄 Context: Git repository • Python project • 5 recent cmd │
│ 💾 Session: merge-conflict-help (Auto-saved)               │
├─────────────────────────────────────────────────────────────┤
│ 💬 You: I have a merge conflict in main.py, how do I fix?  │
│                                                             │
│ 🤖 AI: I can see you just ran `git merge feature-branch`   │
│ and got a conflict in `src/main.py`. Here's how to fix it: │
│                                                             │
│ 1. **Open the conflicted file:**                           │
│    ```bash                                                  │
│    vim src/main.py              [📋 Copy] [▶️ Run]         │
│    ```                                                      │
│                                                             │
│ 2. **Look for conflict markers:**                          │
│    ```                                                      │
│    <<<<<<< HEAD                                             │
│    your changes                                             │
│    =======                                                  │
│    incoming changes                                         │
│    >>>>>>> feature-branch                                   │
│    ```                                                      │
│                                                             │
│ 3. **After editing, mark as resolved:**                    │
│    ```bash                                                  │
│    git add src/main.py          [📋 Copy] [▶️ Run]         │
│    git commit                   [📋 Copy] [▶️ Run]         │
│    ```                                                      │
│                                                             │
│ Would you like me to check the file content first?         │
│                                                             │
│ [🔍 Check File] [📝 Edit Guide] [💾 Save Help] [🔄 Refresh]│
├─────────────────────────────────────────────────────────────┤
│ 💬 Ask AI: _                                               │
│ [📎 Attach Command Output] [🎯 Quick Actions] [⚙️ Settings] │
└─────────────────────────────────────────────────────────────┘
```

### 4. Advanced AI Features

#### Smart Command Suggestions
```python
class SmartSuggestionEngine:
    """Provides intelligent command suggestions based on context"""
    
    def __init__(self, ai_client: AIClient, context: AIContextManager):
        self.ai_client = ai_client
        self.context = context
        self.suggestion_cache = {}
    
    def get_command_suggestions(self, partial_command: str) -> List[Suggestion]:
        """Get AI-powered command suggestions"""
        
        context_prompt = self._build_context_prompt()
        suggestion_prompt = f"""
        Based on the current context and partial command '{partial_command}',
        suggest 3-5 relevant completions with explanations.
        
        Context: {context_prompt}
        
        Return suggestions in JSON format with command and explanation.
        """
        
        suggestions = self.ai_client.get_suggestions(suggestion_prompt)
        return self._parse_suggestions(suggestions)
    
    def get_error_help(self, failed_command: str, error_output: str) -> str:
        """Get AI help for failed commands"""
        
        help_prompt = f"""
        The command '{failed_command}' failed with this error:
        {error_output}
        
        Current context: {self._build_context_prompt()}
        
        Provide specific steps to fix this error.
        """
        
        return self.ai_client.get_help(help_prompt)
```

#### Proactive AI Assistance
```python
class ProactiveAssistant:
    """Provides proactive help based on user patterns"""
    
    def __init__(self, context: AIContextManager):
        self.context = context
        self.pattern_detector = PatternDetector()
        self.help_triggers = self._load_help_triggers()
    
    def check_for_help_opportunities(self):
        """Check if user might need proactive help"""
        
        recent_commands = self.context.terminal_context.recent_commands[-5:]
        
        # Detect struggling patterns
        if self._detect_repeated_failures(recent_commands):
            return self._suggest_help_for_failures()
        
        if self._detect_complex_workflow(recent_commands):
            return self._suggest_workflow_optimization()
        
        if self._detect_new_tool_usage(recent_commands):
            return self._suggest_tool_guidance()
        
        return None
    
    def _detect_repeated_failures(self, commands: List[Command]) -> bool:
        """Detect if user is struggling with repeated failures"""
        failure_count = sum(1 for cmd in commands if cmd.exit_code != 0)
        return failure_count >= 3
```

### 5. AI Window Workflow Enhancements

#### Quick Actions Panel
```python
class QuickActionsPanel:
    """Provides quick actions for common AI interactions"""
    
    def __init__(self, ai_window: AIWindow):
        self.ai_window = ai_window
        self.actions = {
            "explain_last_command": self._explain_last_command,
            "fix_last_error": self._fix_last_error,
            "suggest_next_steps": self._suggest_next_steps,
            "analyze_project": self._analyze_project_structure,
            "git_help": self._provide_git_help,
            "debug_help": self._provide_debug_help
        }
    
    def _explain_last_command(self):
        """Explain the last executed command"""
        last_cmd = self.ai_window.context.terminal_context.recent_commands[-1]
        query = f"Explain what this command does: {last_cmd.command}"
        self.ai_window.send_query(query)
    
    def _fix_last_error(self):
        """Help fix the last command error"""
        last_cmd = self.ai_window.context.terminal_context.recent_commands[-1]
        if last_cmd.exit_code != 0:
            query = f"This command failed: {last_cmd.command}\nError: {last_cmd.output}\nHow do I fix it?"
            self.ai_window.send_query(query)
```

#### Context-Aware Templates
```python
CONTEXT_TEMPLATES = {
    "git_workflow": {
        "triggers": ["git status", "git add", "git commit"],
        "template": "I'm working on a Git workflow. Current status:\n{git_status}\nWhat should I do next?"
    },
    
    "debugging_session": {
        "triggers": ["error", "failed", "exception"],
        "template": "I'm debugging an issue. Recent commands:\n{recent_commands}\nLast error:\n{error_output}\nHelp me troubleshoot."
    },
    
    "project_setup": {
        "triggers": ["npm init", "pip install", "cargo new"],
        "template": "I'm setting up a new {project_type} project. What are the next steps and best practices?"
    }
}
```

## Integration with Terminal Window

### 1. Seamless Data Flow
```python
class TerminalAIBridge:
    """Bridges terminal and AI window for seamless integration"""
    
    def __init__(self, terminal_window: TerminalWindow, ai_window: AIWindow):
        self.terminal_window = terminal_window
        self.ai_window = ai_window
        self.auto_context_update = True
    
    def on_command_executed(self, command: str, output: str, exit_code: int):
        """Update AI context when terminal command executes"""
        
        if self.auto_context_update:
            self.ai_window.context.update_terminal_context(command, output, exit_code)
        
        # Auto-trigger AI help for errors if enabled
        if exit_code != 0 and self.ai_window.config.get('auto_help_on_error'):
            self.ai_window.offer_error_help(command, output)
    
    def send_command_to_terminal(self, command: str, execute: bool = False):
        """Send command from AI window to terminal"""
        
        self.terminal_window.insert_command(command)
        if execute:
            self.terminal_window.execute_current_command()
```

### 2. Cross-Window Actions
```python
class CrossWindowActions:
    """Actions that work across terminal and AI windows"""
    
    def __init__(self, window_manager: WindowManager):
        self.window_manager = window_manager
    
    def execute_ai_suggestion(self, command: str):
        """Execute AI-suggested command in terminal"""
        terminal = self.window_manager.get_window("terminal")
        terminal.execute_command(command)
    
    def explain_terminal_output(self, output: str):
        """Ask AI to explain terminal output"""
        ai_window = self.window_manager.get_window("ai_chat")
        query = f"Explain this command output:\n{output}"
        ai_window.send_query(query)
    
    def create_snippet_from_conversation(self):
        """Create reusable snippet from AI conversation"""
        ai_window = self.window_manager.get_window("ai_chat")
        conversation = ai_window.get_current_conversation()
        snippet = self._extract_useful_commands(conversation)
        self._save_snippet(snippet)
```

## Benefits Over Current System

### 1. **Persistent Context**
- AI remembers entire session conversation
- No context loss when switching between terminal and AI
- Builds understanding over time

### 2. **Parallel Workflows**  
- Use terminal while AI processes responses
- No mode switching required
- Natural conversation flow

### 3. **Enhanced Context Awareness**
- AI automatically knows about recent commands
- Project-aware assistance
- Error context automatically included

### 4. **Interactive Responses**
- Click to execute suggested commands
- Copy code snippets easily
- Save useful conversations

### 5. **Proactive Assistance**
- AI offers help before being asked
- Detects common patterns and struggles
- Suggests optimizations and best practices

This dedicated AI window design transforms TermSage from a simple AI-enhanced terminal into a true AI-powered development environment where the AI becomes a persistent, context-aware assistant that enhances rather than interrupts the natural terminal workflow.
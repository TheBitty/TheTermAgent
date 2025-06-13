# Command Unification Implementation Guide

## Overview
This guide explains how to unify command formats in TermSage by changing `exit` to `/exit` to match other commands like `/chat`, `/models`, etc.

## Implementation Details

### 1. Command Registry Updates
Modified `src/command_registry.py` to standardize command formats:

#### Main Commands Dictionary
```python
# Before
self.commands: Dict[str, Callable] = {
    "exit": self.handle_exit,
    "help": self.handle_help,
    "/tutorial": self.handle_tutorial,
    # ...
}

# After
self.commands: Dict[str, Callable] = {
    "/exit": self.handle_exit,
    "help": self.handle_help,
    "/tutorial": self.handle_tutorial,
    # ...
}
```

#### Chat Commands Dictionary
```python
# Before
self.chat_commands = {
    "/exit": self.exit_chat,
    "exit": self.exit_chat,  # Removed duplicate
    "/clear": self.clear_chat,
    "/help": self.help_chat,
}

# After
self.chat_commands = {
    "/exit": self.exit_chat,
    "/clear": self.clear_chat,
    "/help": self.help_chat,
}
```

## Command Format Standards

### Unified Format Pattern
All TermSage-specific commands now follow the `/command` format:

- `/exit` - Exit the application
- `/chat` - Enter chat mode
- `/tutorial` - Run interactive tutorial
- `/setup` - Run setup wizard
- `/models` - List available AI models
- `/config` - Show configuration
- `/clear` - Clear chat context (in chat mode)
- `/help` - Show help (in chat mode)

### System Commands
System commands remain unchanged (no prefix):
- `ls`, `cd`, `pwd`, `git`, etc.
- `help` - Show main help (system-level)
- `clear` - Clear terminal screen

## Benefits

1. **Consistency**: All TermSage commands use the same `/` prefix
2. **Clarity**: Easy to distinguish between system and TermSage commands
3. **Reduced Confusion**: No ambiguity between `exit` and system commands
4. **Better UX**: Predictable command patterns for users

## Backward Compatibility

- The old `exit` command will no longer work
- Users will need to use `/exit` instead
- This change affects both normal and chat modes

## Files Modified

- `src/command_registry.py`: Updated command dictionaries

## User Impact

### What Users Need to Know
- Use `/exit` instead of `exit` to quit TermSage
- All TermSage-specific commands start with `/`
- System commands remain unchanged

### Help Text Updates
The help system should be updated to reflect the new command format:
- Show `/exit` in command listings
- Update examples and documentation
- Consider adding migration hints for existing users

## Testing Checklist

- [ ] `/exit` works in normal mode
- [ ] `/exit` works in chat mode  
- [ ] Old `exit` command no longer works
- [ ] All other `/` commands still function
- [ ] Help text shows correct commands
- [ ] No regression in system command execution
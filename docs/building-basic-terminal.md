# Building a Basic Terminal Loop

## Overview
This guide walks through creating the foundational terminal loop for TermSage - a working terminal that can execute commands and display output.

## Core Requirements
- Python 3.8+
- subprocess module (built-in)
- Basic understanding of stdin/stdout

## Step-by-Step Implementation

### 1. Basic Terminal Loop Structure
The terminal needs to:
- Display a prompt
- Read user input
- Execute the command
- Show output/errors
- Repeat until user exits

### 2. Key Components

#### Command Execution
Use `subprocess.run()` with proper parameters:
- `shell=True` for shell interpretation
- `capture_output=True` to get stdout/stderr
- `text=True` for string output (not bytes)
- `cwd` to maintain current directory

#### Directory Management
Terminal needs to handle `cd` commands specially since subprocess runs in isolation:
- Track current working directory
- Update it when user runs `cd`
- Pass it to subprocess for each command

#### Exit Handling
Gracefully handle:
- `exit` command
- Ctrl+C (KeyboardInterrupt)
- Ctrl+D (EOFError)

### 3. Implementation Outline

```python
import subprocess
import os
import sys

def run_terminal():
    current_dir = os.getcwd()
    
    while True:
        try:
            # Display prompt with current directory
            prompt = f"{current_dir}$ "
            user_input = input(prompt)
            
            # Handle empty input
            if not user_input.strip():
                continue
                
            # Handle exit
            if user_input.strip() in ['exit', 'quit']:
                break
                
            # Handle cd command
            if user_input.strip().startswith('cd'):
                # Parse and change directory
                # Update current_dir
                
            # Execute other commands
            else:
                result = subprocess.run(
                    user_input,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=current_dir
                )
                
                # Display output
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    print(result.stderr, end='', file=sys.stderr)
                    
        except KeyboardInterrupt:
            print("\n^C")
            continue
        except EOFError:
            print("\nexit")
            break
```

### 4. Special Command Handling

#### cd Command
- Parse arguments (handle `cd`, `cd ~`, `cd ..`, etc.)
- Resolve paths relative to current_dir
- Validate path exists
- Update current_dir on success

#### Built-in Commands
Some commands need special handling:
- `clear` - Clear terminal screen
- `history` - Show command history (requires tracking)
- `pwd` - Can use Python's os.getcwd()

### 5. Error Handling

- **Invalid commands**: Let subprocess show the error
- **Permission errors**: Display clearly
- **Path errors**: Show helpful messages
- **Malformed input**: Catch and continue

### 6. Testing Your Terminal

Test these scenarios:
1. Basic commands: `ls`, `pwd`, `echo hello`
2. Directory navigation: `cd /tmp`, `cd ..`, `cd ~`
3. Piping: `ls | grep txt`
4. Error cases: `invalidcommand`, `cd /nonexistent`
5. Exit methods: `exit`, Ctrl+C, Ctrl+D

### 7. Next Steps

Once the basic loop works:
1. Add command history with arrow keys
2. Implement tab completion for files
3. Add the `?` suffix detection for AI help
4. Integrate AI providers
5. Build auto-completion system

## Important Notes

- Start simple - just get commands executing
- Don't add features until basic execution works
- Test thoroughly on your target OS
- Keep the loop responsive (no blocking operations)
- Maintain clear separation between terminal and future AI features

## Common Pitfalls

1. **Forgetting shell=True**: Commands won't work properly
2. **Not handling cd**: Users get confused when directory doesn't change
3. **Blocking on long commands**: Terminal appears frozen
4. **Not preserving output formatting**: Breaks tools like `ls -la`
5. **Overcomplicating early**: Add features incrementally

Remember: A working terminal that can run `ls` is better than a complex system that doesn't work yet.
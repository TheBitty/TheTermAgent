# TermSage User Guide

## How It Works

### Normal Terminal Usage
TermSage functions exactly like any standard terminal. You can run all your regular commands:

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
Add intelligence to your terminal experience with these features:

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
Enhanced tab completion that learns from your usage:

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

## Usage Examples

### Getting Help with Commands
```bash
# Don't know how to use a command?
tar?
# AI explains: "tar is used for archiving files. Common usage:
# - Create archive: tar -czf archive.tar.gz files/
# - Extract: tar -xzf archive.tar.gz
# - List contents: tar -tzf archive.tar.gz"

# Complex command help
ffmpeg?
# AI provides detailed ffmpeg examples for common tasks
```

### Troubleshooting Errors
```bash
# When a command fails
$ npm install
# Error: EACCES permission denied
# AI suggests: "Try using 'sudo npm install' or better yet, 
# configure npm to use a different directory: npm config set prefix ~/.npm"
```

### Interactive Learning
```bash
/chat
> "How do I find which process is using port 8080?"

AI: You can use several commands:
1. lsof -i :8080
2. netstat -tulpn | grep 8080
3. ss -tulpn | grep 8080
The lsof command is most direct and will show the PID.

> "What's the difference between apt and apt-get?"

AI: apt is the newer, more user-friendly command...
```

### Smart Workflows
```bash
# AI learns your patterns
$ git add .
$ git commit -m "feat: add new feature"
# Next time you type 'git add .', AI might suggest:
# "Follow up with: git commit -m 'your message'"

# Context-aware suggestions
$ cd ~/projects/website
$ [Tab][Tab]
# AI suggests relevant commands based on project type:
# npm start, npm test, npm build, git status
```

## Tips and Tricks

### 1. Use ? Liberally
Don't remember a command's syntax? Just add ? to get instant help without leaving the terminal.

### 2. Let AI Debug for You
When commands fail, the AI automatically analyzes the error and suggests fixes. No need to search online.

### 3. Chat for Complex Tasks
Use `/chat` when you need to discuss a complex problem or learn about a topic in depth.

### 4. Customize AI Behavior
Switch between AI models based on your needs:
- Local models (Ollama) for privacy
- Cloud models for advanced features

### 5. Command Chaining
The AI understands context, so you can ask about related commands:
```bash
git?  # Get git help
# Then ask about specific workflows
> "How do I undo the last commit?"
```

## Common Use Cases

### Development Workflow
```bash
# AI helps with common dev tasks
docker-compose?     # Container management
pytest?            # Running tests
npm?               # Package management
git?               # Version control
```

### System Administration
```bash
# Get help with system tasks
systemctl?         # Service management
cron?             # Scheduling tasks
iptables?         # Firewall rules
htop?             # Process monitoring
```

### File Management
```bash
# Smart file operations
find?             # Searching files
rsync?            # Syncing data
tar?              # Archiving
chmod?            # Permissions
```

### Network Debugging
```bash
# Network troubleshooting
ping?             # Connectivity tests
curl?             # HTTP requests
netstat?          # Network statistics
tcpdump?          # Packet analysis
```

## Privacy and Security

### Local AI Models
- Use Ollama for completely offline AI assistance
- No data leaves your machine
- Full privacy for sensitive work

### Command Validation
- TermSage validates dangerous commands
- Prompts for confirmation on destructive operations
- Prevents accidental data loss

### Secure Practices
- AI never stores passwords or secrets
- Command history can be configured
- Sandbox mode for testing
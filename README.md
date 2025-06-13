# 🚀 TermAgent (TermSage)

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)

**Your terminal, but smarter.** TermAgent is an AI-enhanced terminal that helps you when you're stuck, without getting in your way when you're not.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## 🎯 What is TermAgent?

Ever found yourself:
- 🤔 Googling command syntax for the hundredth time?
- 😤 Fighting with cryptic error messages?
- 📚 Digging through man pages for that one flag?
- 🔍 Trying to remember how to use `tar`, `find`, or `rsync`?

**TermAgent solves this.** It's your regular terminal with an AI assistant built right in. When you need help, just ask. When you don't, it stays out of your way.

### Key Benefits

- **Zero Learning Curve**: Works exactly like your current terminal
- **Instant Help**: Add `?` to any command for explanations
- **Smart Error Analysis**: Automatic suggestions when commands fail
- **Privacy First**: Run everything locally with Ollama, or use cloud AI
- **Cross-Platform**: Works on Linux, macOS, and Windows

## ✨ Features

### 🔍 **Instant Command Help**
Just add `?` to any command to get explanations, examples, and options:
```bash
git?              # Explains git commands relevant to your current repo
docker?           # Docker help tailored to your running containers
find?             # No more struggling with find syntax
tar?              # Finally understand tar flags
```

### 💬 **Interactive Chat Mode**
Need to talk through a problem? Enter chat mode:
```bash
/chat
> How do I find all large files in my home directory?
> What's the best way to backup my photos but skip thumbnails?
> Help me write a script to organize my downloads folder
```

### 🛠️ **Smart Error Analysis**
When commands fail, TermAgent automatically analyzes the error and suggests fixes:
```bash
$ git push origin main
error: failed to push some refs to 'origin'

💡 TermAgent: "Your local branch is behind the remote. Try:
   git pull --rebase origin main
   Then resolve any conflicts and push again."
```

### 🎨 **Enhanced Terminal Experience**
- **Auto-completion** with AI-powered suggestions
- **Command history** with intelligent search
- **Contextual tips** based on your current directory
- **Project awareness** (detects git repos, node projects, python environments)

### 🔒 **Privacy & Flexibility**
- **Local AI Models**: Use Ollama for complete privacy
- **Cloud Options**: Connect to OpenAI, Anthropic, or other providers
- **Configurable**: Choose your model, adjust settings, customize behavior

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/TermAgent.git
cd TermAgent

# Run the installer
chmod +x run.sh
./run.sh
```

That's it! The installer will:
- ✅ Check Python version (3.8+ required)
- ✅ Install dependencies
- ✅ Set up configuration
- ✅ Download AI models (if using Ollama)
- ✅ Start TermAgent

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Install Ollama for local AI
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama2  # or your preferred model

# Run TermAgent
cd src
python main.py
```

### Docker Installation

```bash
# Coming soon!
docker run -it termagent/termagent:latest
```

## 🚀 Usage

### Basic Commands

Once TermAgent is running, use it like any normal terminal:

```bash
# All your regular commands work
ls -la
cd ~/projects
git status
npm install

# Get help by adding ?
git?                    # Explains git in context of current repo
docker ps?              # Explains docker ps and your containers
find . -name "*.py"?    # Explains this specific find command

# Built-in commands
help                    # Show all TermAgent commands
/chat                   # Enter interactive chat mode
/model llama2           # Switch AI model
/tutorial               # Interactive tutorial for new users
/exit                   # Exit TermAgent
```

### Configuration

TermAgent stores configuration in `~/.termagent/config.json`:

```json
{
  "ai": {
    "provider": "ollama",
    "model": "llama2",
    "ollama_url": "http://localhost:11434"
  },
  "terminal": {
    "enable_help": true,
    "enable_error_analysis": true,
    "enable_autocomplete": true,
    "start_with_sudo": false
  },
  "ui": {
    "show_tips": true,
    "color_output": true
  }
}
```

### Advanced Features

#### **Working with Projects**
TermAgent automatically detects project types and provides contextual help:

```bash
# In a Git repository
git?  # Shows branch info, staged changes, and relevant commands

# In a Node.js project
npm?  # Shows available scripts from package.json

# In a Python project
pip?  # Shows virtual environment info and installed packages
```

#### **Command Chaining**
Get help for complex command pipelines:

```bash
"ps aux | grep python | awk '{print $2}'"?
# Explains each part of the pipeline
```

#### **Learning Mode**
Perfect for beginners:

```bash
/tutorial
# Interactive tutorial covering:
# - Basic terminal navigation
# - File operations
# - Git basics
# - And more!
```

## 📚 Examples

### Example 1: Debugging Git Issues

```bash
$ git push
To github.com:user/repo.git
 ! [rejected]        main -> main (non-fast-forward)

💡 TermAgent: "Your push was rejected because the remote has changes you don't have locally.

Options:
1. If you want to keep remote changes:
   git pull --rebase origin main
   
2. If you're sure your version is correct:
   git push --force origin main
   
3. To see what's different:
   git fetch origin
   git diff main origin/main"

$ git pull --rebase origin main
Successfully rebased and updated refs/heads/main.
```

### Example 2: Finding Files

```bash
$ find?
💡 TermAgent: "Here are common find examples for your current directory:

Find files by name:
  find . -name "*.py"           # Find all Python files
  find . -name "config*"        # Find files starting with 'config'

Find by size:
  find . -size +10M             # Files larger than 10MB
  find . -size -1k              # Files smaller than 1KB

Find by time:
  find . -mtime -7              # Modified in last 7 days
  find . -newer reference.txt   # Newer than reference.txt"
```

### Example 3: Interactive Problem Solving

```bash
$ /chat
🤖 Chat mode activated. Type 'exit' to return to terminal.

You: I need to free up disk space but not sure what's taking up room

TermAgent: I'll help you identify what's using disk space. Here are the most effective approaches:

1. Check overall disk usage:
   df -h

2. Find large directories:
   du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20

3. Find large files:
   find / -type f -size +100M 2>/dev/null | head -20

4. For a visual representation, you could install 'ncdu':
   sudo apt install ncdu  # Debian/Ubuntu
   ncdu /

Would you like me to explain any of these commands or help you with a specific directory?

You: Let's check my home folder specifically

TermAgent: Here's how to analyze your home folder:

du -h --max-depth=1 ~/ | sort -hr | head -10

This will show the 10 largest directories in your home folder. Let me know what you find and I can help you safely clean up space!
```

## 🛠️ Development

### Project Structure

```
TermAgent/
├── src/
│   ├── main.py              # Entry point and main loop
│   ├── command_handler.py   # Command execution engine
│   ├── command_registry.py  # Built-in command routing
│   ├── ollama_helper.py     # AI integration layer
│   ├── config.py            # Configuration management
│   ├── ui_utils.py          # Terminal UI and formatting
│   ├── help_system.py       # Tutorial and help system
│   ├── onboarding.py        # First-time setup wizard
│   └── decorators.py        # Utility decorators
├── tests/
│   └── test_*.py            # Test files
├── AI Docs/                 # Development documentation
│   ├── API_Summary.md       # API documentation
│   ├── Architecture.md      # System design
│   └── ...
├── Specs/                   # Feature specifications
├── .claude/                 # AI assistant context
├── run.sh                   # Quick start script
└── requirements.txt         # Python dependencies
```

### Adding New Features

1. **Plan Your Feature**
   ```bash
   cp Specs/Feature_Template.md Specs/YourFeature.md
   # Edit the template with your feature details
   ```

2. **Implement Following Conventions**
   - Follow naming conventions in `AI Docs/Coding_Conventions.md`
   - Add tests for new functionality
   - Update documentation

3. **Example: Adding a New Command**
   ```python
   # In command_registry.py
   class CommandRegistry:
       def __init__(self, ui, ollama_helper):
           self.commands = {
               # ... existing commands ...
               "/yourcommand": self.handle_your_command,
           }
       
       def handle_your_command(self, args: str) -> bool:
           """Handle the /yourcommand command."""
           # Your implementation here
           self.ui.print_info("Your command executed!")
           return False  # False continues terminal, True exits
   ```

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_command_handler.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Code Style

- Follow PEP 8
- Use type hints
- Document all public methods
- Global variables: `g_variable_name`
- Constants: `c_CONSTANT_NAME`

## 🤝 Contributing

We love contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow coding conventions
   - Add tests
   - Update documentation
4. **Submit a pull request**

### Areas We Need Help

- 🌍 **Internationalization**: Help translate TermAgent
- 🎨 **Themes**: Create custom color themes
- 🔌 **Plugins**: Develop plugin system and plugins
- 📚 **Documentation**: Improve guides and examples
- 🐛 **Bug Fixes**: Help squash bugs
- ✨ **Features**: Implement features from our roadmap

## 📈 Roadmap

### Version 1.0 (Current)
- ✅ Basic terminal functionality
- ✅ AI help with `?` suffix
- ✅ Chat mode
- ✅ Error analysis
- ✅ Ollama integration

### Version 1.1 (In Progress)
- 🔄 Enhanced auto-completion
- 🔄 Plugin system
- 🔄 Custom themes
- 🔄 Performance improvements

### Version 2.0 (Planned)
- 📋 Multi-language support
- 📋 Remote execution (SSH)
- 📋 Team collaboration features
- 📋 Advanced scripting assistance
- 📋 Voice commands

## 🆘 Troubleshooting

### Common Issues

**TermAgent won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check for errors
python src/main.py --debug
```

**AI features not working**
```bash
# For Ollama users
ollama list  # Check installed models
ollama pull llama2  # Install a model

# Check configuration
cat ~/.termagent/config.json
```

**Commands not executing**
```bash
# Check shell compatibility
echo $SHELL

# Try with explicit shell
python src/main.py --shell /bin/bash
```

For more help, see `AI Docs/Troubleshooting.md` or open an issue.

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local AI
- Inspired by the Unix philosophy
- Thanks to all contributors!

---

<div align="center">

**Ready to make your terminal smarter?** [Get Started](#-installation)

[Report Bug](https://github.com/yourusername/TermAgent/issues) • [Request Feature](https://github.com/yourusername/TermAgent/issues) • [Documentation](AI%20Docs/)

</div>
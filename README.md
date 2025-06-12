# TermSage - AI-Enhanced Terminal

TermSage is an intelligent terminal that enhances your command-line experience with AI assistance. It works exactly like your regular terminal but adds powerful AI features to help you be more productive.

## ✨ Features

### 🤖 **AI-Powered Help**
- Add `?` to any command for instant AI explanations (e.g., `git?`, `docker?`)
- Get contextual help based on your current directory and project type
- Automatic error analysis with suggested fixes

### 💬 **Interactive Chat Mode**
- Type `/chat` to start AI conversations about terminal tasks
- Ask complex questions like "How do I find large files?" or "Help me write a backup script"
- Natural language interaction for learning new commands

### 🎨 **Enhanced User Experience**
- **Colorized Output**: Success (green), errors (red), AI responses (cyan)
- **Loading Indicators**: Visual feedback during AI operations
- **Smart Prompts**: Shows current mode (normal/chat) and directory
- **Interactive Tutorial**: First-time walkthrough of all features

### 🚀 **Smart Features**
- **Auto-completion**: Enhanced tab completion with AI suggestions
- **Command History**: Intelligent history with pattern learning
- **Contextual Tips**: Helpful suggestions based on your workflow
- **Safety Checks**: Prevents dangerous operations with confirmation prompts

### ⚙️ **Easy Setup**
- **Onboarding Wizard**: Guided first-time setup
- **Auto-configuration**: Detects available AI models automatically
- **Multiple AI Models**: Support for various Ollama models
- **Flexible Configuration**: Customize behavior to your preferences

## 🛠 Installation

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd TermAgent

# Make the launcher executable
chmod +x run.sh

# Run TermSage (installs dependencies automatically)
./run.sh
```

### Manual Installation
```bash
# Install Python dependencies
pip install requests

# Run from source directory
cd src
python main.py
```

### Requirements
- Python 3.8+
- Ollama (optional, for AI features)
  - Install from: https://ollama.com/download
  - Quick install: `curl -fsSL https://ollama.com/install.sh | sh`

## 🚀 Usage

### Basic Commands
```bash
# Get help for any command
git?                 # Learn git commands and workflows
docker?              # Docker help and examples
tar?                 # Archive command explanations

# Start AI chat mode
/chat                # Interactive AI conversations
> "How do I monitor CPU usage?"
> "Help me write a bash script"

# Interactive features
/tutorial            # Complete feature walkthrough
/setup               # Re-run setup wizard
help                 # Show all commands
```

### Example Workflow
```bash
# Regular terminal usage works exactly the same
ls -la
cd ~/projects
git status

# Add AI help when needed
systemctl?           # "How do I manage services?"
find?                # "Help me search for files"

# Chat for complex tasks
/chat
> "I need to backup my home directory excluding cache files"
> "What's the best way to monitor disk usage over time?"
```

## 🎯 Key Benefits

- **Zero Learning Curve**: Works exactly like your regular terminal
- **Instant Help**: No need to search online for command syntax
- **Error Recovery**: AI suggests fixes when commands fail
- **Learning Tool**: Gradually learn new commands with AI guidance
- **Privacy Option**: Use local Ollama models - no data leaves your machine

## 📁 Project Structure

```
TermAgent/
├── src/                      # Core application
│   ├── main.py              # Main terminal loop  
│   ├── ui_utils.py          # Enhanced UI and colors
│   ├── command_registry.py  # Command handling system
│   ├── help_system.py       # Tutorial and help features
│   ├── onboarding.py        # Setup wizard
│   ├── ollama_helper.py     # AI integration
│   ├── config.py           # Configuration management
│   ├── command_handler.py   # Command execution
│   └── decorators.py        # Utility decorators
├── AI Docs/                 # Comprehensive documentation
├── Specs/                   # Feature specifications  
├── requirements.txt         # Dependencies
├── run.sh                   # Launch script
└── README.md               # This file
```

## 🤝 Contributing

We welcome contributions! Please see our documentation in `AI Docs/` for:
- `Coding_Conventions.md` - Code style guidelines
- `Project_Architecture.md` - Technical architecture
- `Feature_Template.md` - How to plan new features

## 📜 License

This project is licensed under the MIT License.

## 🆘 Getting Help

1. **In TermSage**: Type `help` or `/tutorial`
2. **Documentation**: Check the `AI Docs/` directory
3. **Issues**: Report bugs or request features via GitHub issues

---

*Ready to supercharge your terminal experience? Run `./run.sh` and type `/tutorial` to get started!*# TermAgent

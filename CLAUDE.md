# TermSage - Quick Reference Guide

## 📁 Documentation Structure

### AI Docs/ - Comprehensive Documentation
- **[API_Summary.md](AI%20Docs/API_Summary.md)** - External API documentation and integration details
- **[Coding_Conventions.md](AI%20Docs/Coding_Conventions.md)** - Code style guidelines and standards
- **[Configuration_Guide.md](AI%20Docs/Configuration_Guide.md)** - Configuration options and settings
- **[Project_Architecture.md](AI%20Docs/Project_Architecture.md)** - System design and technical architecture
- **[Troubleshooting.md](AI%20Docs/Troubleshooting.md)** - Common issues and debugging strategies
- **[User_Guide.md](AI%20Docs/User_Guide.md)** - How to use TermSage effectively

### Specs/ - Feature Specifications
- **[Feature_Template.md](Specs/Feature_Template.md)** - Template for planning new features

### .claude/ - AI Context Priming
- **[prime.sh](.claude/prime.sh)** - Shell script for loading project context
- **[prime.md](.claude/prime.md)** - Markdown prompt for AI initialization

### Other Key Files
- **[AI_DOCS.md](AI_DOCS.md)** - AI memory and session-specific learnings
- **[README.md](README.md)** - User-facing documentation

## 🚀 Quick Start

### For AI Assistants
1. Run `.claude/prime.sh` or read `.claude/prime.md` to load full context
2. Review `AI_DOCS.md` for project overview and recent learnings
3. Check relevant documentation in `AI Docs/` based on the task

### For Developers
1. Read `AI Docs/Project_Architecture.md` for system design
2. Follow `AI Docs/Coding_Conventions.md` for code standards
3. Use `Specs/Feature_Template.md` when planning new features
4. Consult `AI Docs/Troubleshooting.md` when debugging

## 🔑 Key Concepts

### Core Principles
- **Terminal First** - Full terminal functionality is primary
- **Non-Intrusive AI** - AI enhances but doesn't interfere
- **Performance** - Fast and responsive operations
- **Cross-Platform** - Works on Linux, macOS, Windows

### Naming Conventions
- Global Variables: `g_VARIABLE_NAME`
- Constants: `c_CONSTANT_NAME`
- Classes: `PascalCase`
- Functions: `snake_case`

### AI Integration
- Command help with `?` suffix (e.g., `git?`)
- Chat mode with `/chat`
- Auto-completion with AI suggestions
- Automatic error analysis

## 📊 Project Status
- ✅ Basic terminal functionality
- ✅ Command execution and safety
- ✅ AI model integration
- ✅ Auto-completion system
- 🔄 Enhanced AI suggestions
- 🔄 Cross-platform compatibility
- 📋 Advanced context management
- 📋 Performance optimizations

---
*This is a quick reference guide. For detailed information, explore the documentation in the directories listed above.*
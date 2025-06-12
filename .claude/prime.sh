#!/bin/bash
# This script/prompt is designed to prime the AI with essential project context.
# It instructs the AI to read key documentation and specifications.

echo "=== AI Context Priming Script ==="
echo "Initializing AI assistant with project context..."
echo ""

# 1. Read the main project README for an overview.
echo "📖 Reading README.md for project overview..."
# In actual AI tool usage, this would be: read_file README.md
echo "Command: read_file README.md"
echo ""

# 2. Read the CLAUDE.md file for AI-specific context
echo "🤖 Reading CLAUDE.md for AI context and guidelines..."
echo "Command: read_file CLAUDE.md"
echo ""

# 3. Read the AI_DOCS.md for retained information from previous sessions
echo "🧠 Reading AI_DOCS.md for session memory..."
echo "Command: read_file AI_DOCS.md"
echo ""

# 4. Recursively read the AI Docs directory for persistent knowledge.
echo "📚 Reading AI Docs directory for project conventions and knowledge..."
# In actual AI tool usage, this would be: read_directory "AI Docs"
echo "Command: read_directory \"AI Docs\""
echo "  - API_Summary.md"
echo "  - Coding_Conventions.md"
echo "  - Troubleshooting.md"
echo ""

# 5. Recursively read the Specs directory for any existing project plans.
echo "📋 Reading Specs directory for existing project plans..."
# In actual AI tool usage, this would be: read_directory Specs
echo "Command: read_directory Specs"
echo "  - Feature_Template.md"
echo "  - [Any feature specs]"
echo ""

# 6. Check current git status for context
echo "🔍 Checking git status..."
echo "Command: git status"
echo ""

# 7. Review recent commits for context
echo "📜 Reviewing recent commits..."
echo "Command: git log --oneline -10"
echo ""

# 8. Scan source code structure
echo "🏗️ Scanning source code structure..."
echo "Command: ls -la src/"
echo ""

# 9. Check for any TODO items or issues
echo "✅ Checking for TODO items..."
echo "Command: grep -r \"TODO\\|FIXME\\|XXX\" src/ 2>/dev/null || echo 'No TODOs found'"
echo ""

# 10. Load user preferences if they exist
echo "⚙️ Loading user configuration..."
echo "Command: read_file config.user.json 2>/dev/null || echo 'No user config found'"
echo ""

echo "=== Context Priming Complete ==="
echo ""
echo "✨ I am now aware of:"
echo "  • Project structure and architecture (TermSage terminal)"
echo "  • Coding conventions and style guidelines"
echo "  • API integrations and external services"
echo "  • Common issues and troubleshooting procedures"
echo "  • Feature specification templates and planning process"
echo "  • Current git status and recent changes"
echo "  • Project-specific naming conventions (g_, c_ prefixes)"
echo ""
echo "Ready to assist with TermSage development!"
echo ""

# Additional context reminders
echo "🔔 Key Reminders:"
echo "  • Terminal functionality is the primary feature"
echo "  • AI enhancements should be non-intrusive"
echo "  • Follow established naming conventions"
echo "  • Prioritize performance and cross-platform compatibility"
echo "  • Always validate user commands for safety"
echo ""

# Note for actual AI tool implementation:
# Replace echo commands with actual AI tool API calls:
# - read_file: Read single file content
# - read_directory: Recursively read directory contents
# - execute_command: Run shell commands for dynamic context
# 
# Example AI tool syntax (adapt to your specific tool):
# await ai.read_file("README.md")
# await ai.read_directory("AI Docs")
# await ai.execute_command("git status")
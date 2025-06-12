# AI Context Priming Prompt

## Initialize Project Context

Please read and internalize the following project documentation to understand the TermSage terminal application:

### 1. Project Overview
Read `README.md` to understand:
- What TermSage is (AI-enhanced terminal)
- Core features and functionality
- Installation and usage instructions

### 2. AI-Specific Context
Read `CLAUDE.md` to understand:
- Project philosophy and goals
- Development guidelines
- Code style and naming conventions
- Current implementation status

### 3. Session Memory
Read `AI_DOCS.md` to recall:
- Previous session learnings
- Important technical details
- User interaction patterns

### 4. Technical Documentation
Read all files in `AI Docs/` directory:
- **API_Summary.md**: External API details and usage
- **Coding_Conventions.md**: Project standards and patterns
- **Troubleshooting.md**: Common issues and solutions

### 5. Project Specifications
Read all files in `Specs/` directory:
- **Feature_Template.md**: How to plan new features
- Any existing feature specifications

### 6. Source Code Context
Examine the `src/` directory structure:
- Main entry point and core modules
- Understand the architecture
- Note any TODOs or FIXMEs

### 7. Current State
Check:
- Git status and recent commits
- Any configuration files
- Test coverage and status

## Key Context Points

After reading the above, you should understand:

1. **Project Goal**: Create a terminal that works normally but has AI help when needed
2. **Architecture**: Modular design with clear separation of concerns
3. **Naming Conventions**:
   - Global variables: `g_VARIABLE_NAME`
   - Constants: `c_CONSTANT_NAME`
   - Classes: `PascalCase`
   - Functions/variables: `snake_case`
4. **AI Integration**: Non-intrusive, optional assistance
5. **Priority**: Terminal functionality first, AI enhancement second

## Development Principles

Remember these core principles:
- **Terminal First**: Must work as a regular terminal
- **Performance**: Keep operations fast and responsive
- **Safety**: Validate dangerous commands
- **Cross-Platform**: Support Linux, macOS, Windows
- **User Experience**: AI helps but never interferes

## Ready State

Once you've absorbed this context, you'll be ready to:
- Implement new features following conventions
- Debug issues using the troubleshooting guide
- Write specs for new functionality
- Maintain code quality and consistency
- Provide helpful, contextual assistance

Please confirm when you've processed this context and are ready to assist with TermSage development.
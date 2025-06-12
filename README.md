# TermSage

You know how you're always googling command syntax or trying to remember the right flags for `tar` or `find`? This fixes that.

TermSage is just your regular terminal, but when you're stuck on something, you can ask for help without leaving your workspace. Add a `?` to any command to get an explanation, or type `/chat` to have a longer conversation about what you're trying to do.

It's not trying to replace your terminal or change how you work. It just sits there quietly until you need it.

## What it does

**Command help with `?`**
Confused about a command? Just add `?` at the end. `git?` explains git stuff, `docker?` helps with Docker, `systemctl?` for services. Works with pretty much anything.

**Chat mode for bigger questions**
Sometimes you need to talk through a problem. Type `/chat` and ask things like "how do I backup my photos but skip the cache files" or "what's eating all my disk space."

**Error analysis**
When something breaks, it looks at the error and suggests what might have gone wrong. No more cryptic messages that make no sense.

**Still your terminal**
Everything works exactly like before. Your aliases, your shell, your muscle memory. The AI stuff only shows up when you ask for it.

## Installation

```bash
git clone <repository-url>
cd TermAgent
chmod +x run.sh
./run.sh
```

That's it. The script installs what it needs and starts up. First time it runs, it'll ask you a few setup questions.

If you want to do it manually:
```bash
pip install requests
cd src
python main.py
```

**Requirements:**
- Python 3.8+
- Ollama (if you want local AI models instead of cloud ones)

To get Ollama: `curl -fsSL https://ollama.com/install.sh | sh`

## How to use it

Once it's running, just use your terminal like normal. When you need help:

```bash
# Regular terminal stuff works fine
ls -la
cd ~/projects
git status

# Stuck on something? Add a ?
git?                 # explains git commands
docker?              # docker help
find?                # how to search for files

# Need to talk through a problem?
/chat
> "I want to backup my home folder but skip cache files"
> "What's using all my disk space?"
> "Help me write a script to organize my downloads"

# See what else you can do
help                 # shows all commands
/tutorial            # walks through the features
```

## Example

Say you're trying to push some code and it fails:

```bash
$ git push origin main
error: failed to push some refs to 'origin'

# TermSage sees the error and suggests:
"Looks like there are conflicts. Try 'git pull --rebase origin main' 
first, resolve conflicts, then push."

# Want more details?
git?
# explains your git situation

# Or get help working through it:
/chat
> "I'm getting merge conflicts and don't want to mess anything up"
```

## Why this is useful

You don't have to learn anything new or change how you work. When you're stuck, the help is right there instead of having to google around or dig through man pages.

If you're privacy-conscious, you can run everything locally with Ollama. If you want more powerful AI, you can use cloud services. Your choice.

## Code structure

```
TermAgent/
├── src/
│   ├── main.py              # main terminal loop
│   ├── ui_utils.py          # colors and UI stuff
│   ├── command_registry.py  # handles commands
│   ├── help_system.py       # tutorial and help
│   ├── onboarding.py        # first-time setup
│   ├── ollama_helper.py     # talks to AI models
│   ├── config.py           # settings
│   ├── command_handler.py   # runs commands safely
│   └── decorators.py        # utility functions
├── AI Docs/                 # project docs
├── tests/                   # tests
├── run.sh                  # launcher script
└── README.md               # this file
```

## How it works

The `?` suffix gets intercepted before your command runs, so it doesn't interfere with anything. Chat mode switches to a different input handler. Error analysis happens automatically in the background.

Supports Ollama for local models (llama2, codellama, mistral) or cloud AI services.

## Contributing

The code is pretty straightforward. UI stuff is in `ui_utils.py`, AI integration is in `ollama_helper.py`, and commands are handled through a registry pattern in `command_registry.py`.

Check the `AI Docs/` folder for more detailed info.

## Support

Type `help` in TermSage to see commands, or `/tutorial` for a walkthrough.

For bugs or questions, use GitHub issues.

## License

MIT

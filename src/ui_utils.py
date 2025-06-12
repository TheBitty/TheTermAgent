"""
UI Utilities - Colors, formatting, and visual feedback for TermSage
"""

import os
import sys
import time
import threading
from typing import Optional
from enum import Enum

class Color(Enum):
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

class UIUtils:
    """Utility class for enhanced terminal UI"""
    
    def __init__(self):
        # Check if colors are supported
        self.colors_enabled = self._supports_color()
    
    def _supports_color(self) -> bool:
        """Check if terminal supports ANSI colors"""
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
            'TERM' in os.environ and os.environ['TERM'] != 'dumb'
        )
    
    def colorize(self, text: str, color: Color, bold: bool = False) -> str:
        """Apply color to text if colors are supported"""
        if not self.colors_enabled:
            return text
        
        color_code = color.value
        if bold:
            color_code = Color.BOLD.value + color_code
        
        return f"{color_code}{text}{Color.RESET.value}"
    
    def format_message(self, text: str, msg_type: str) -> str:
        """Format message with appropriate icon and color"""
        message_config = {
            "success": ("✓", Color.BRIGHT_GREEN),
            "error": ("✗", Color.BRIGHT_RED), 
            "warning": ("⚠", Color.BRIGHT_YELLOW),
            "info": ("ℹ", Color.BRIGHT_BLUE),
            "ai": ("🤖", Color.BRIGHT_CYAN)
        }
        
        icon, color = message_config.get(msg_type, ("", Color.WHITE))
        return self.colorize(f"{icon} {text}", color)
    
    def success(self, text: str) -> str:
        """Format success message in green"""
        return self.format_message(text, "success")
    
    def error(self, text: str) -> str:
        """Format error message in red"""
        return self.format_message(text, "error")
    
    def warning(self, text: str) -> str:
        """Format warning message in yellow"""
        return self.format_message(text, "warning")
    
    def info(self, text: str) -> str:
        """Format info message in blue"""
        return self.format_message(text, "info")
    
    def ai_response(self, text: str) -> str:
        """Format AI response in cyan"""
        return self.format_message(text, "ai")
    
    def command(self, text: str) -> str:
        """Format command in bold"""
        return self.colorize(text, Color.WHITE, bold=True)
    
    def prompt(self, text: str) -> str:
        """Format prompt in magenta"""
        return self.colorize(text, Color.BRIGHT_MAGENTA)
    
    def dim(self, text: str) -> str:
        """Format text as dimmed"""
        if not self.colors_enabled:
            return text
        return f"{Color.DIM.value}{text}{Color.RESET.value}"

class LoadingIndicator:
    """Animated loading indicator for long operations"""
    
    def __init__(self, message: str = "Processing", ui_utils: Optional[UIUtils] = None):
        self.message = message
        self.ui_utils = ui_utils or UIUtils()
        self.is_running = False
        self.thread = None
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.frame_index = 0
    
    def start(self):
        """Start the loading animation"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop the loading animation"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.thread:
            self.thread.join()
        
        # Clear the line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def _animate(self):
        """Animation loop"""
        while self.is_running:
            frame = self.frames[self.frame_index]
            spinner_text = f"\r{self.ui_utils.colorize(frame, Color.BRIGHT_BLUE)} {self.message}..."
            sys.stdout.write(spinner_text)
            sys.stdout.flush()
            
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            time.sleep(0.1)

def print_banner():
    """Print TermSage banner with styling"""
    ui = UIUtils()
    banner = f"""
{ui.colorize('╔══════════════════════════════════════════════════╗', Color.BRIGHT_CYAN)}
{ui.colorize('║', Color.BRIGHT_CYAN)} {ui.colorize('TermSage', Color.BRIGHT_WHITE, bold=True)} - AI-Enhanced Terminal                    {ui.colorize('║', Color.BRIGHT_CYAN)}
{ui.colorize('╚══════════════════════════════════════════════════╝', Color.BRIGHT_CYAN)}

{ui.info('Welcome to your intelligent terminal assistant!')}
{ui.dim('Type "help" for a complete guide or try these quick examples:')}

  {ui.command('git?')}          {ui.dim('→ Get help with git commands')}
  {ui.command('/chat')}         {ui.dim('→ Start AI conversation mode')}
  {ui.command('docker?')}       {ui.dim('→ Learn docker commands')}
  {ui.command('/tutorial')}     {ui.dim('→ Interactive feature walkthrough')}
"""
    print(banner)

def show_help():
    """Display comprehensive help information"""
    ui = UIUtils()
    help_text = f"""
{ui.colorize('TermSage Help', Color.BRIGHT_WHITE, bold=True)}
{ui.colorize('═' * 50, Color.BRIGHT_CYAN)}

{ui.colorize('🚀 QUICK START', Color.BRIGHT_YELLOW, bold=True)}
  {ui.command('help')}              Show this help message
  {ui.command('/tutorial')}         Interactive feature walkthrough
  {ui.command('command?')}          Get AI help for any command (e.g., git?, docker?)
  {ui.command('/chat')}             Start conversational AI mode
  {ui.command('exit')}              Exit TermSage

{ui.colorize('🤖 AI FEATURES', Color.BRIGHT_YELLOW, bold=True)}
  {ui.command('<command>?')}        Get contextual help for any command
  {ui.command('/chat')}             Interactive AI conversation
  {ui.command('/models')}           List available AI models
  {ui.command('/model <name>')}     Switch AI model
  {ui.command('/config')}           Show current configuration
  
  {ui.dim('Examples:')}
    {ui.command('tar?')}            {ui.dim('→ Learn tar command usage')}
    {ui.command('ffmpeg?')}         {ui.dim('→ Get ffmpeg examples')}
    {ui.command('systemctl?')}      {ui.dim('→ Service management help')}

{ui.colorize('💡 SMART FEATURES', Color.BRIGHT_YELLOW, bold=True)}
  • {ui.success('Auto Error Analysis')}: Failed commands get AI suggestions
  • {ui.success('Contextual Help')}: AI understands your current directory
  • {ui.success('Command History')}: Smart history with AI enhancement
  • {ui.success('Safety Checks')}: Prevents dangerous operations

{ui.colorize('🔧 TERMINAL OPERATIONS', Color.BRIGHT_YELLOW, bold=True)}
  {ui.command('clear')}             Clear screen
  {ui.command('history')}           Show command history
  {ui.command('cd <path>')}         Change directory
  
  {ui.dim('All standard terminal commands work exactly as expected!')}

{ui.colorize('⚙️ CONFIGURATION', Color.BRIGHT_YELLOW, bold=True)}
  Config file: {ui.dim('~/.termsage/config.json')}
  History file: {ui.dim('~/.termsage/history')}
  
  {ui.command('/config')}           View current settings
  {ui.command('/model llama2')}     Switch to different AI model

{ui.colorize('💬 CHAT MODE COMMANDS', Color.BRIGHT_YELLOW, bold=True)}
  {ui.command('/exit')}             Exit chat mode
  {ui.command('/clear')}            Clear conversation
  {ui.command('/help')}             Chat mode help

{ui.colorize('🆘 GETTING HELP', Color.BRIGHT_YELLOW, bold=True)}
  • Add {ui.command('?')} to any command for instant help
  • Use {ui.command('/chat')} for complex troubleshooting
  • Check the User Guide: {ui.dim('AI Docs/User_Guide.md')}
  
{ui.dim('Pro tip: TermSage learns from your usage patterns to provide better suggestions!')}
"""
    print(help_text)
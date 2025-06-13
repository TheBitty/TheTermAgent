"""
Command Handler - Executes system commands
"""

import os
import subprocess
import shlex


class CommandResult:
    """Container for command execution results"""

    def __init__(self, stdout: str = "", stderr: str = "", exit_code: int = 0):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.returncode = exit_code  # For compatibility


class CommandHandler:
    """Handles command execution and special commands"""

    def __init__(self):
        """Initialize command handler"""
        self.last_exit_code = 0

    def execute(self, command: str) -> CommandResult:
        """
        Execute a system command

        Args:
            command: Command string to execute

        Returns:
            CommandResult with output and exit code
        """
        # Handle empty command
        if not command.strip():
            return CommandResult()

        # Handle cd command specially (it needs to change the Python process's directory)
        if command.startswith("cd "):
            return self._handle_cd(command)

        # Handle cd with no arguments (go to home)
        if command.strip() == "cd":
            return self._handle_cd("cd ~")

        # Execute other commands via subprocess
        try:
            # Run command in shell mode to support pipes, redirects, etc.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                # Use the current working directory
                cwd=os.getcwd(),
            )

            # Store exit code for reference
            self.last_exit_code = result.returncode

            # Print output (stdout and stderr)
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="")

            # Return result for potential AI analysis
            return CommandResult(stdout=result.stdout, stderr=result.stderr, exit_code=result.returncode)

        except Exception as e:
            error_msg = f"Command execution failed: {e}"
            print(error_msg)
            self.last_exit_code = 1
            return CommandResult(stderr=error_msg, exit_code=1)

    def _handle_cd(self, command: str) -> CommandResult:
        """
        Handle cd command to change directory

        Args:
            command: cd command string

        Returns:
            CommandResult
        """
        # Extract path from command
        parts = shlex.split(command)
        if len(parts) < 2:
            # cd with no args goes to home
            path = os.path.expanduser("~")
        else:
            path = parts[1]

        # Expand special paths
        path = os.path.expanduser(path)  # Expand ~
        path = os.path.expandvars(path)  # Expand environment variables

        try:
            # Change directory
            os.chdir(path)
            self.last_exit_code = 0
            return CommandResult(exit_code=0)

        except FileNotFoundError:
            error_msg = f"cd: no such file or directory: {path}"
            print(error_msg)
            self.last_exit_code = 1
            return CommandResult(stderr=error_msg, exit_code=1)

        except PermissionError:
            error_msg = f"cd: permission denied: {path}"
            print(error_msg)
            self.last_exit_code = 1
            return CommandResult(stderr=error_msg, exit_code=1)

        except Exception as e:
            error_msg = f"cd: {e}"
            print(error_msg)
            self.last_exit_code = 1
            return CommandResult(stderr=error_msg, exit_code=1)

    def get_last_exit_code(self) -> int:
        """Get the exit code of the last executed command"""
        return self.last_exit_code


# Root Startup Implementation Guide

## Overview
This guide explains how to modify TermSage to automatically start with root (sudo) privileges.

## Implementation Details

### 1. Root Privilege Check Function
Added `ensure_root_startup()` function in `src/main.py`:

```python
def ensure_root_startup():
    """Ensure the terminal starts with root privileges if needed"""
    import subprocess
    
    # Check if we're already running as root
    if os.geteuid() != 0:
        # We're not root, need to restart with sudo
        print("Starting TermSage with root privileges...")
        try:
            # Get the current script path
            script_path = os.path.abspath(__file__)
            # Restart with sudo
            subprocess.run(['sudo', 'python3', script_path] + sys.argv[1:])
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nCancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"Failed to start with root privileges: {e}")
            print("Continuing without root privileges...")
```

### 2. Integration into Main Function
Modified `main()` function to call root check at startup:

```python
def main():
    """Main terminal loop"""
    # Ensure root startup
    ensure_root_startup()
    
    # Initialize components...
```

## How It Works

1. **Check Current Privileges**: Uses `os.geteuid()` to check if running as root (UID = 0)
2. **Restart with Sudo**: If not root, restarts the script with `sudo python3`
3. **Preserve Arguments**: Passes through all command-line arguments
4. **Graceful Fallback**: If sudo fails, continues without root privileges
5. **User Control**: Allows cancellation with Ctrl+C

## Benefits

- Commands requiring root privileges work seamlessly
- No need to manually prefix with `sudo`
- System administration tasks become more convenient
- Maintains security by requiring initial sudo permission

## Security Considerations

- Users must still enter their password for the initial sudo prompt
- Root privileges are only requested at startup
- Script can still run without root if sudo fails
- Users can cancel the root request

## Files Modified

- `src/main.py`: Added root startup functionality

## Testing

1. Run TermSage normally - it should prompt for sudo password
2. Cancel the sudo prompt - should continue without root
3. Verify root commands work when running with sudo
4. Test that non-root functionality still works
import os
import sys

def run_as_root():
    """
    Checks if the script is running as root and re-runs with sudo if necessary.
    """
    if os.getuid() != 0:
        #print("Not running as root. Attempting to re-run with sudo...")
        try:
            # Replaces the current process with a new process using sudo
            # sys.executable is the path to the current Python interpreter
            # sys.argv are the arguments passed to the script
            os.execvp("sudo", ["sudo", sys.executable, *sys.argv])
        except FileNotFoundError:
            print("The 'sudo' command was not found. Cannot elevate privileges.")
            sys.exit(1)
        except PermissionError:
            print("Permission denied to run sudo. Check your /etc/sudoers file.")
            sys.exit(1)
    else:
        pass
        #print("Running as root (UID 0).")
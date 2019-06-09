import sys

# Modified version of https://github.com/barneygale/elevate/

def elevate(show_console=True):
    """
    Re-launch the current process with root/admin privileges

    When run as root, this function does nothing.

    When not run as root, this function replaces the current process (Linux,
    macOS) or creates a child process, waits, and exits (Windows).

    :param show_console: (Windows only) if True, show a new console for the
        child process. Ignored on Linux / macOS.
    :param graphical: (Linux / macOS only) if True, attempt to use graphical
        programs (gksudo, etc). Ignored on Windows.
    """
    if sys.platform.startswith("win"):
        from habu.lib.elevate.windows import elevate
    else:
        from habu.lib.elevate.posix import elevate

    elevate(show_console)


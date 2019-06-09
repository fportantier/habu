import errno
import os
import sys
try:
    from shlex import quote
except ImportError:
    from pipes import quote


def quote_shell(args):
    return " ".join(quote(arg) for arg in args)


def quote_applescript(string):
    charmap = {
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\"": "\\\"",
        "\\": "\\\\",
    }
    return '"%s"' % "".join(charmap.get(char, char) for char in string)


def elevate(show_console=True):
    if os.getuid() == 0:
        return

    args = [sys.executable] + sys.argv

    command = ["sudo"] + args

    try:
        os.execlp(command[0], *args)
    except OSError as e:
        if e.errno != errno.ENOENT or args[0] == "sudo":
            raise

#!/usr/bin/env python3

import shlex
import subprocess
import sys
from pathlib import Path
from shutil import which
from time import sleep


def web_screenshot(url, outfile):

    if not which('firefox'):
        print('You don\'t have firefox in your PATH.', file=sys.stderr)
        return False

    outfile = Path(outfile)

    profile_cmd = shlex.split('firefox --new-instance --CreateProfile habu.web.screenshot')
    screenshot_cmd = shlex.split('firefox --new-instance --headless -P habu.web.screenshot --screenshot {} {}'.format(outfile, url))

    subprocess.Popen(profile_cmd, stderr=subprocess.DEVNULL)

    try:
        outfile.unlink()
    except FileNotFoundError:
        pass

    with subprocess.Popen(screenshot_cmd, stderr=subprocess.DEVNULL) as proc:

        for i in range(20):

            sleep(1)

            if outfile.is_file():
                break

            if i == 19:
                print('Error', file=sys.stderr)
                return False

        proc.kill()

    return True

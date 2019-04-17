#!/usr/bin/env python3

import shlex
import subprocess
import sys
from pathlib import Path
from shutil import which
from time import sleep

DURATION = 20


def web_screenshot(url, outfile, browser):
    """Create a screenshot of a website."""
    if not which(browser):
        print("You don't have {} in your PATH".format(browser), file=sys.stderr)
        return False

    screenshot_cmd = ''
    profile_firefox = shlex.split('firefox --new-instance --CreateProfile habu.web.screenshot')
    screenshot_firefox = shlex.split('firefox --new-instance --headless -P habu.web.screenshot --screenshot {} {}'.format(outfile, url))
    screenshot_chromium = shlex.split('chromium-browser --headless --disable-gpu --window-size=1440,900 --screenshot={} {}'.format(outfile, url))

    if browser == 'firefox':
        screenshot_cmd = screenshot_firefox
        subprocess.Popen(profile_firefox, stderr=subprocess.DEVNULL)

    if browser == 'chromium-browser':
        screenshot_cmd = screenshot_chromium

    outfile = Path(outfile)
    if outfile.is_file():
        outfile.unlink()

    with subprocess.Popen(screenshot_cmd, stderr=subprocess.DEVNULL) as proc:
        for count in range(DURATION):
            sleep(1)
            if outfile.is_file():
                break

            if count == DURATION - 1:
                print("Unable to create screenshot", file=sys.stderr)
                break

        proc.kill()
    return True

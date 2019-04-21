#!/usr/bin/env python3

import shlex
import subprocess
import sys
from pathlib import Path
from shutil import which
from time import sleep

DURATION = 20

def web_screenshot(url, outfile, browser=None):
    """Create a screenshot of a website."""

    valid_browsers = ['firefox', 'chromium-browser']
    available_browsers = [ b for b in valid_browsers if which(b) ]

    if not available_browsers:
        print("You don't have firefox or chromium-browser in your PATH".format(browser), file=sys.stderr)
        return False

    if not browser:
        browser = available_browsers[0]

    if browser not in available_browsers:
        print("You don't have {} in your PATH".format(browser), file=sys.stderr)
        return False

    #screenshot_cmd = ''
    #profile_firefox = shlex.split('firefox --new-instance --CreateProfile habu.web.screenshot')
    #screenshot_firefox = shlex.split('firefox --new-instance --headless -P habu.web.screenshot --screenshot {} {}'.format(outfile, url))
    #screenshot_chromium = shlex.split('chromium-browser --headless --disable-gpu --window-size=1440,900 --screenshot={} {}'.format(outfile, url))

    if browser == 'firefox':
        profile_firefox = shlex.split('firefox --new-instance --CreateProfile habu.web.screenshot')
        subprocess.Popen(profile_firefox, stderr=subprocess.DEVNULL)
        screenshot_cmd = shlex.split('firefox --new-instance --headless -P habu.web.screenshot --screenshot {} {}'.format(outfile, url))

    if browser == 'chromium-browser':
        screenshot_cmd = shlex.split('chromium-browser --headless --disable-gpu --window-size=1440,900 --screenshot={} {}'.format(outfile, url))

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


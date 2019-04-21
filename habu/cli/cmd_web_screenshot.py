#!/usr/bin/env python3

import shlex
import subprocess
import sys
from pathlib import Path
from shutil import which
from time import sleep

import click

from habu.lib.web_screenshot import web_screenshot


@click.command()
@click.argument('url')
@click.option('-b', 'browser', default=None, type=click.Choice(['firefox', 'chromium-browser']), help='Browser to use for screenshot.')
@click.option('-o', 'outfile', default='screenshot.png', help='Output file. (default: screenshot.png)')
def cmd_web_screenshot(url, outfile, browser):
    """Uses Firefox or Chromium to take a screenshot of the website.

    \b
    $ habu.web.screenshot https://www.portantier.com
    """

    web_screenshot(url, outfile, browser=browser)

if __name__ == '__main__':
    cmd_web_screenshot()

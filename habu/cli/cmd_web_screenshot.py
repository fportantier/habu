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
@click.option('-o', 'outfile', default='screenshot.png', help='Output file. (default: screenshot.png)')
def cmd_web_screenshot(url, outfile):
    """Uses Firefox to take a screenshot (you need firefox installed, obviously)

    \b
    $ habu.web.screenshot https://www.portantier.com
    """

    web_screenshot(url, outfile)

if __name__ == '__main__':
    cmd_web_screenshot()

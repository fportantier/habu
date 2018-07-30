#!/usr/bin/env python3

import json
import sys

import click

from pathlib import Path

from habu.lib.xor import xor
from habu.config import config

from habu.lib.loadcfg import loadcfg

from cryptography.fernet import Fernet


@click.command()
@click.option('-w', 'writecfg', is_flag=True, default=False, help='Write this key to ~/.habu.json')
def cmd_fernet_genkey(writecfg):
    """Generate a new Fernet Key, optionally write it to ~/.habu.json

    Example:

    \b
    $ habu.fernet.genkey
    xgvWCIvjwe9Uq7NBvwO796iI4dsGD623QOT9GWqnuhg=
    """

    key = Fernet.generate_key()
    print(key.decode())

    if writecfg:
        habucfg = loadcfg(environment=False)
        habucfg['FERNET_KEY'] = key.decode()
        with Path('~/.habu.json').expanduser().open('w') as f:
            f.write(json.dumps(habucfg, indent=4, sort_keys=True))

if __name__ == '__main__':
    cmd_fernet_genkey()


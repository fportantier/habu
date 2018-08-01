#!/usr/bin/env python3

import sys

import click

from habu.lib.xor import xor
from habu.config import config

from habu.lib.loadcfg import loadcfg

from cryptography.fernet import Fernet

ERROR_NOKEY = '''A key must be provided. You have the following options:
    1. Use the -k option with a valid key
    2. Save an existing key to ~/.habu.json file (variable FERNET_KEY)
    3. Export the environment variable HABU_FERNET_KEY

To generate a valid key, you can use habu.fernet.genkey
'''


@click.command()
@click.option('-k', 'key', default=None, help='Key')
@click.option('-d', 'decrypt', is_flag=True, default=False, help='Decrypt instead of encrypt')
@click.option('--ttl', 'ttl', default=0, type=click.INT, help='Time To Live for timestamp verification')
@click.option('-i', type=click.File('rb'), default='-', help='Input file (default: stdin)')
@click.option('-o', type=click.File('wb'), default='-', help='Output file (default: stdout)')
def cmd_fernet(key, decrypt, ttl, i, o):
    """Fernet cipher.

    Uses AES-128-CBC with HMAC

    Note: You must use a key to cipher with Fernet.

    Use the -k paramenter or set the FERNET_KEY configuration value.

    The keys can be generated with the command habu.fernet.genkey

    Reference: https://github.com/fernet/spec/blob/master/Spec.md

    Example:

    \b
    $ "I want to protect this string" | habu.fernet
    gAAAAABbXnCGoCULLuVNRElYTbEcwnek9iq5jBKq9JAN3wiiBUzPqpUgV5oWvnC6xfIA...

    \b
    $ echo gAAAAABbXnCGoCULLuVNRElYTbEcwnek9iq5jBKq9JAN3wiiBUzPqpUgV5oWvnC6xfIA... | habu.fernet -d
    I want to protect this string
    """

    habucfg = loadcfg()

    if not key:
        if 'FERNET_KEY' in habucfg:
            key = habucfg['FERNET_KEY']
        else:
            print(ERROR_NOKEY, file=sys.stderr)
            sys.exit(1)

    if not ttl:
        ttl=None

    cipher = Fernet(key)

    data = i.read()

    if decrypt:
        try:
            token = cipher.decrypt(data, ttl)
        except Exception as e:
            print("Error decrypting", file=sys.stderr)
            sys.exit(1)
    else:
        token = cipher.encrypt(data)

    print(token.decode(), end='')

if __name__ == '__main__':
    cmd_fernet()


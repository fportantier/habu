#!/usr/bin/env python3

import base64
import os
import sys

import click


@click.command()
@click.argument('f', type=click.File('rb'), default='-')
@click.option('-d', 'do_decode', is_flag=True, default=False, help='decode instead of encode')
def cmd_b64(f, do_decode):
    """
    This command encodes/decodes data in base64, just like the command base64.

    \b
    $ echo awesome | habu.b64
    YXdlc29tZQo=

    \b
    $ echo YXdlc29tZQo= | habu.b64 -d
    awesome
    """

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    if do_decode:
        os.write(sys.stdout.fileno(), base64.b64decode(data))
    else:
        os.write(sys.stdout.fileno(), base64.b64encode(data))


if __name__ == '__main__':
    cmd_b64()

#!/usr/bin/env python3

import click

from habu.lib.hasher import ALGOS, hasher


@click.command()
@click.argument('f', type=click.File('rb'), default='-')
@click.option('-a', 'algorithm', default=None, type=click.Choice(ALGOS), help='Only this algorithm (Default: all)')
def cmd_hasher(f, algorithm):
    """This command computes various hashes for the input data, that can be a
    file or a stream.

    Example:

    \b
    $ habu.hasher README.rst
    md5         : e5828c564f71fea3a12dde8bd5d27063
    ripemd160   : ef6886c3b68cb34a44f9ca9336f3cd0732600a84
    sha1        : 7bae8076a5771865123be7112468b79e9d78a640
    sha512      : 65cfb1cf719b851b4aea5a7f5388068687b1fdfd290817a...
    whirlpool   : eaccf718b31d8a01f76fc08e896a6d0d73dbeafc2621fe0...

    You can also specify which algorithm to use. In such case, the output is
    only the value of the calculated hash:

    \b
    $ habu.hasher -a md5 README.rst
    e5828c564f71fea3a12dde8bd5d27063
    """

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    if algorithm:
        print(hasher(data, algorithm)[algorithm])
    else:
        for algo, result in hasher(data).items():
            print("{:<12}: {}".format(algo, result))

if __name__ == '__main__':
    cmd_hasher()

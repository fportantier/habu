#!/usr/bin/env python3

import click

from habu.lib.hasher import ALGOS, hasher


@click.command()
@click.argument('f', type=click.File('rb'), default='-')
@click.option('-a', 'algorithm', default=None, type=click.Choice(ALGOS), help='Only this algorithm (Default: all)')
def cmd_hasher(f, algorithm):
    """Compute various hashes for the input data, that can be a file or a stream.

    Example:

    \b
    $ habu.hasher README.rst
    md5          992a833cd162047daaa6a236b8ac15ae README.rst
    ripemd160    0566f9141e65e57cae93e0e3b70d1d8c2ccb0623 README.rst
    sha1         d7dbfd2c5e2828eb22f776550c826e4166526253 README.rst
    sha256       6bb22d927e1b6307ced616821a1877b6cc35e... README.rst
    sha512       8743f3eb12a11cf3edcc16e400fb14d599b4a... README.rst
    whirlpool    96bcc083242e796992c0f3462f330811f9e8c... README.rst

    You can also specify which algorithm to use. In such case, the output is
    only the value of the calculated hash:

    \b
    $ habu.hasher -a md5 README.rst
    992a833cd162047daaa6a236b8ac15ae README.rst
    """

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    if algorithm:
        print(hasher(data, algorithm)[algorithm], f.name)
    else:
        for algo, result in hasher(data).items():
            print("{:<12} {} {}".format(algo, result, f.name))


if __name__ == '__main__':
    cmd_hasher()

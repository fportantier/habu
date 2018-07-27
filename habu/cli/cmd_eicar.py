#!/usr/bin/env python3

import click

from habu.lib.eicar import eicar


@click.command()
def cmd_eicar():
    """Print the EICAR test string that can be used to test antimalware engines.

    More info: http://www.eicar.org/86-0-Intended-use.html

    Example:

    \b
    $ habu.eicar
    X5O!P%@AP[4\XZP54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
    """

    print(eicar())

if __name__ == '__main__':
    cmd_eicar()

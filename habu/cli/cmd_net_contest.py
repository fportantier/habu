#!/usr/bin/env python3

import click

from habu.lib import contest


@click.command()
def cmd_net_contest():
    """Try to connect to various services and check if can
    reach them using your internet connection.

    Example:

    \b
    $ habu.net.contest
    DNS:   True
    FTP:   True
    SSH:   True
    HTTP:  True
    HTTPS: True"""

    print("DNS:   %s" % contest.check_dns())
    print("FTP:   %s" % contest.check_ftp())
    print("SSH:   %s" % contest.check_ssh())
    print("HTTP:  %s" % contest.check_http())
    print("HTTPS: %s" % contest.check_https())


if __name__ == '__main__':
    cmd_net_contest()

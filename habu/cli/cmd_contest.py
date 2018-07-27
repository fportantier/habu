#!/usr/bin/env python3

import click

from habu.lib import contest


@click.command()
def cmd_contest():
    """This command tries to connect to various services and check if you can
    reach them using your internet connection.

    Example:

    \b
    $ habu.contest
    IP:    True
    DNS:   True
    FTP:   True
    SSH:   True
    HTTP:  True
    HTTPS: True"""

    print("IP:    %s" % contest.check_ip())
    print("DNS:   %s" % contest.check_dns())
    print("FTP:   %s" % contest.check_ftp())
    print("HTTP:  %s" % contest.check_http())
    print("HTTPS: %s" % contest.check_https())


if __name__ == '__main__':
    cmd_contest()

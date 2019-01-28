#!/usr/bin/env python3

import logging
import random

import click

from habu.lib.loadcfg import loadcfg


@click.command()
@click.option('-l', 'lowest', type=click.IntRange(1,65534, clamp=True), default=1025, help='Lowest port to consider')
@click.option('-h', 'highest', type=click.IntRange(2,65535, clamp=True), default=65535, help='Highest port to consider')
def cmd_nmap_excluded(lowest, highest):
    """
    Prints a random port that is not present on nmap-services file so is not scanned automatically by nmap.

    Useful for services like SSH or RDP, that are continuously scanned on their default ports.

    Example:

    \b
    # habu.nmap.excluded
    58567
    """

    if lowest >= highest:
        logging.error('lowest can not be greater or equal than highest')

    cfg = loadcfg()

    with (cfg['DATADIR'] / 'nmap-services').open() as nsf:
        nmap_services = nsf.read()

    unwanted = set()

    for line in nmap_services.strip().split('\n'):
        if line.startswith('#'):
            continue

        service,port,_ = line.split('\t', maxsplit=2)
        unwanted.add(int(port.split('/')[0]))

    choices = list(range(lowest,highest))
    random.shuffle(choices)

    found = False
    for choice in choices:
        if choice not in unwanted:
            print(choice)
            found = True
            break

    if not found:
        logging.error('Can\'t find a port number with the specified parameters')

if __name__ == '__main__':
    cmd_nmap_excluded()

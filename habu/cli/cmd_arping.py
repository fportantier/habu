#!/usr/bin/env python3

import logging
import re
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, IP, TCP, Ether, conf, srp


@click.command()
@click.argument('ip')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_arping(ip, iface, verbose):
    """
    This command send ARP packets to check if a host it's alive in the local network.

    Example:

    \b
    # habu.arping 192.168.0.1
    Ether / ARP is at a4:08:f5:19:17:a4 says 192.168.0.1 / Padding
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    conf.verb = False

    if iface:
        conf.iface = iface

    res, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2)

    for _, pkt in res:
        if verbose:
            print(pkt.show())
        else:
            print(pkt.summary())


if __name__ == '__main__':
    cmd_arping()

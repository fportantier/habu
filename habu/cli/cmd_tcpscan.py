#!/usr/bin/env python3

import logging
import re
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import IP, TCP, conf, sr, sr1


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default='80', help='Ports to use (default: 80) example: 20-23,80,135')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-f', 'flags', default='S', help='Flags to use (default: S)')
@click.option('-s', 'sleeptime', default=None, help='Time between probes (default: send all together)')
@click.option('-t', 'timeout', default=2, help='Timeout for each probe (default: 2 seconds)')
@click.option('-a', 'show_all', is_flag=True, default=False, help='Show all responses (default: Only containing SYN flag)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_tcpscan(ip, port, iface, flags, sleeptime, timeout, show_all, verbose):
    """TCP Port Scanner.

    Prints the ports that generated a response with the SYN flag or (if show use -a) all the
    ports that generated a response.

    It's really basic compared with nmap, but who is comparing?

    Example:

    \b
    # habu.tcpscan -p 22,23,80,443 -s 1 45.77.113.133
    22 S -> SA
    80 S -> SA
    443 S -> SA
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    conf.verb = False

    if iface:
        conf.iface = iface

    port_regex = r'^[0-9,-]+$'

    if not re.match(port_regex, port):
        logging.critical("Invalid port specification")
        return False

    ports = []

    for p in str(port).split(','):
        if '-' in p:
            first, last = p.split('-')
            for n in range(int(first), int(last)+1):
                ports.append(n)
        else:
            ports.append(int(p))

    out = "{port} {sflags} -> {rflags}"

    pkts = IP(dst=ip)/TCP(flags=flags, dport=ports)

    if sleeptime:
        res = []
        for pkt in pkts:
            logging.info(pkt.summary())
            _ = sr1(pkt)
            if _:
                logging.info(_.summary())
                res.append((pkt, _))
    else:
        res, unans = sr(pkts, verbose=verbose)

    for s,r in res:
        if show_all or 'S' in r.sprintf(r"%TCP.flags%"):
            print(out.format(
                port=s[TCP].dport,
                sflags=s.sprintf(r"%TCP.flags%"),
                rflags=r.sprintf(r"%TCP.flags%")
            ))

if __name__ == '__main__':
    cmd_tcpscan()

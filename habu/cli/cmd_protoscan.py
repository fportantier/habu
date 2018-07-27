#!/usr/bin/env python3

import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import IP, conf, sr


@click.command()
@click.argument('ip')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-t', 'timeout', default=2, help='Timeout for each probe (default: 2 seconds)')
@click.option('--all', 'all_protocols', is_flag=True, default=False, help='Probe all protocols (default: Defined in /etc/protocols)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_ipscan(ip, iface, timeout, all_protocols, verbose):
    """
    Send IP packets with different protocol field content to guess what
    layer 4 protocols are available.

    The output shows which protocols doesn't generate a 'protocol-unreachable'
    ICMP response.

    Example:

    \b
    $ sudo python cmd_ipscan.py 45.77.113.133
    1   icmp
    2   igmp
    4   ipencap
    6   tcp
    17  udp
    41  ipv6
    47  gre
    50  esp
    51  ah
    58  ipv6_icmp
    97  etherip
    112 vrrp
    115 l2tp
    132 sctp
    137 mpls_in_ip
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    conf.verb = False

    if iface:
        conf.iface = iface

    if all_protocols:
        protocols = (0,255)
    else:
        # convert "{name:num}" to {num:name}"
        protocols = { num:name for name,num in conf.protocols.__dict__.items() if isinstance(num, int) }

    ans,unans=sr(IP(dst=ip, proto=protocols.keys())/"SCAPY", retry=0, timeout=timeout, verbose=verbose)

    allowed_protocols = [ pkt['IP'].proto for pkt in unans ]

    for proto in sorted(allowed_protocols):
        print('{:<4} {}'.format(proto, protocols[proto])) #conf.protocols._find(str(proto))))


if __name__ == '__main__':
    cmd_ipscan()

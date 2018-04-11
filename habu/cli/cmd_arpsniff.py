import logging
from time import time

import click

import habu.lib.manuf

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, IP, TCP, conf, sniff


hosts = {}

mac2vendor = habu.lib.manuf.MacParser()


def procpkt(pkt):

    now = time()
    output = '{seconds}\t{ip}\t{hwaddr}\t{vendor}'

    if 'ARP' in pkt:
        hosts[pkt[ARP].psrc] = {}
        hosts[pkt[ARP].psrc]['hwaddr'] = pkt[ARP].hwsrc
        hosts[pkt[ARP].psrc]['vendor'] = mac2vendor.get_comment(pkt[ARP].hwsrc)
        hosts[pkt[ARP].psrc]['time'] = time()

        click.clear()

        for ip in sorted(hosts):
            print(output.format(
                seconds = int(now - hosts[ip]['time']),
                ip = ip,
                hwaddr = hosts[ip]['hwaddr'],
                vendor = hosts[ip]['vendor']
            ))


@click.command()
@click.option('-i', 'iface', default=None, help='Interface to use')
def cmd_arpsniff(iface):
    """ ARP Sniffer """

    conf.verb = False

    if iface:
        conf.iface = iface

    print("Waiting for ARP packets...")

    sniff(filter="arp", store=False, prn=procpkt)


if __name__ == '__main__':
    cmd_arpsniff()

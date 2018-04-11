import logging
import re
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, conf, sr, sr1


@click.command()
@click.argument('ip')
#@click.option('-p', 'port', default='80', help='Ports to use (default: 80) example: 20-23,80,135')
@click.option('-i', 'iface', default=None, help='Interface to use')
#@click.option('-f', 'flags', default='S', help='Flags to use (default: S)')
@click.option('-s', 'sleeptime', default=None, help='Time between probes (default: send all together)')
@click.option('-t', 'timeout', default=2, help='Timeout for each probe (default: 2 seconds)')
#@click.option('-a', 'show_all', is_flag=True, default=False, help='Show all responses (default: Only containing SYN flag)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_ipscan(ip, iface, sleeptime, timeout, verbose):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    conf.verb = False

    if iface:
        conf.iface = iface

    ans,unans=sr(IP(dst=ip, proto=(0,255))/"SCAPY",retry=0,timeout=2, verbose=True)

    for s,r in ans:
        print(r.summary())
        if not ICMP in r:
            r.show()

if __name__ == '__main__':
    cmd_ipscan()

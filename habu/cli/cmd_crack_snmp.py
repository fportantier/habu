#!/usr/bin/env python3

import logging
import os
import sys
from pathlib import Path

import click
from scapy.all import ASN1_OID, IP, SNMP, UDP, IPv6, SNMPget, SNMPvarbind, conf, sr1

from habu.lib.ip_version import ip_version
from habu.lib.run_as_root import run_as_root

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


@click.command()
@click.argument("ip")
@click.option("-p", "port", default=161, help="Port to use")
@click.option(
    "-c", "community", default=None, help="Community (default: list of most used)"
)
@click.option("-s", "stop", is_flag=True, default=True, help="Stop after first match")
@click.option("-v", "verbose", is_flag=True, default=False, help="Verbose")
def cmd_crack_snmp(ip, community, port, stop, verbose):
    """Launches snmp-get queries against an IP, and tells you when
    finds a valid community string (is a simple SNMP cracker).

    The dictionary used is the distributed with the onesixtyone tool
    https://github.com/trailofbits/onesixtyone

    Example:

    \b
    # habu.crack.snmp 179.125.234.210
    Community found: private
    Community found: public
    """

    run_as_root()

    FILEDIR = os.path.dirname(os.path.abspath(__file__))
    DATADIR = os.path.abspath(os.path.join(FILEDIR, "../data"))
    COMMFILE = Path(os.path.abspath(os.path.join(DATADIR, "dict_snmp.txt")))

    if community:
        communities = [community]
    else:
        with COMMFILE.open() as cf:
            communities = cf.read().split("\n")

    conf.verb = False

    oid = "1.3.6.1"

    if ip_version(ip) == 4:
        layer3 = IP(dst=ip)
    else:
        layer3 = IPv6(dst=ip)

    for pkt in (
        layer3
        / UDP(sport=port, dport=port)
        / SNMP(
            community="public",
            PDU=SNMPget(varbindlist=[SNMPvarbind(oid=ASN1_OID(oid))]),
        )
    ):

        if verbose:
            print(ip)

        for community in communities:

            if verbose:
                print(".", end="")
                sys.stdout.flush()

            pkt[SNMP].community = community
            ans = sr1(pkt, timeout=0.5, verbose=0)

            if ans and UDP in ans:
                if verbose:
                    print(ans.show())
                else:
                    print("\n{} - Community found: {}".format(ip, community))
                if stop:
                    break

    return True


if __name__ == "__main__":
    cmd_crack_snmp()

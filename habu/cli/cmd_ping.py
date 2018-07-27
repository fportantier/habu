#!/usr/bin/env python3

import logging
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, conf, sr1, L3RawSocket


@click.command()
@click.argument('ip')
@click.option('-i', 'interface', default=None, help='Wich interface to use (default: auto)')
@click.option('-c', 'count', default=0, help='How many packets send (default: infinit)')
@click.option('-t', 'timeout', default=2, help='Timeout in seconds (default: 2)')
@click.option('-w', 'wait', default=1, help='How many seconds between packets (default: 1)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_ping(ip, interface, count, timeout, wait, verbose):
    """This command implements the classic 'ping' with ICMP echo requests.

    \b
    # habu.ping 8.8.8.8
    IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
    IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
    IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
    IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
    """

    if interface:
        conf.iface = interface

    conf.verb = False
    conf.L3socket=L3RawSocket

    layer3 = IP()
    layer3.dst = ip
    layer3.tos = 0
    layer3.id = 1
    layer3.flags = 0
    layer3.frag = 0
    layer3.ttl = 64
    layer3.proto = 1 # icmp

    layer4 = ICMP()
    layer4.type = 8 # echo-request
    layer4.code = 0
    layer4.id = 0
    layer4.seq = 0

    pkt = layer3 / layer4

    counter = 0

    while True:
        ans = sr1(pkt, timeout=timeout)
        if ans:
            if verbose:
                ans.show()
            else:
                print(ans.summary())
            del(ans)
        else:
            print('Timeout')

        counter += 1

        if count != 0 and counter == count:
            break

        sleep(wait)

    return True

if __name__ == '__main__':
    cmd_ping()

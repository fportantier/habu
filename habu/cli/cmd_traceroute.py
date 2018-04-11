import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, TCP, UDP, conf, sr1


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-i', 'iface', default=None, help='Interface to use')
def cmd_traceroute(ip, port, iface):

    conf.verb = False

    if iface:
        conf.iface = iface

    pkts = IP(dst=ip, ttl=(1, 16)) / TCP(dport=port)

    for pkt in pkts:

        ans = sr1(pkt, timeout=1, iface=conf.iface)

        if not ans:
            print('.')
            continue

        print(ans.summary())

        if TCP in ans and ans[TCP].flags == 18:
            break

    return True


if __name__ == '__main__':
    cmd_traceroute()

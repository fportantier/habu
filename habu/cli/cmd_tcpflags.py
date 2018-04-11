import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, TCP, conf, sr, sr1


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-f', 'flags', default=None, help='Flags that must be sent ever (default: fuzz with all flags)')
@click.option('-r', 'rflags', default=None, help='Filter by response flags (default: show all responses)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_tcpflags(ip, port, flags, rflags, verbose):

    conf.verb = False

    pkts = IP(dst=ip) / TCP(flags=(0, 255), dport=port)

    out = "{:>8} -> {:<8}"

    for pkt in pkts:
        if not flags or all(i in pkt.sprintf(r"%TCP.flags%") for i in flags):
            ans = sr1(pkt, timeout=0.2)
            if ans:
                if not rflags or all(i in ans.sprintf(r"%TCP.flags%") for i in rflags):
                    print(out.format(pkt.sprintf(r"%TCP.flags%"), ans.sprintf(r"%TCP.flags%")))

    return True

if __name__ == '__main__':
    cmd_tcpflags()

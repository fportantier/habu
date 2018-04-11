import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, TCP, conf, sr, sr1


@click.command()
@click.argument('ip')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_protoscan(ip, verbose):

    conf.verb = False

    #pkts = IP(dst=ip) / TCP(flags=(0, 255), dport=port)
    pkts = IP(dst=ip, proto=(0, 255)) # / TCP(flags=(0, 255), dport=port)

    out = "{:>8} -> {:<8}"

    for pkt in pkts:
        #if not flags or all(i in pkt.sprintf(r"%TCP.flags%") for i in flags):
        print(pkt.show2())
        ans = sr1(pkt, timeout=0.2)
        if ans:
            #if not rflags or all(i in ans.sprintf(r"%TCP.flags%") for i in rflags):
            #print(out.format(pkt.sprintf(r"%TCP.flags%"), ans.sprintf(r"%TCP.flags%")))
            print(ans.show())

    return True

if __name__ == '__main__':
    cmd_protoscan()

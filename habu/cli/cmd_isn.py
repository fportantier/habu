from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, TCP, UDP, RandShort, conf, send, sr1, srloop


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-c', 'count', default=5, help='How many packets to send/receive (default: 5)')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-g', 'graph', is_flag=True, default=False, help='Graph (requires matplotlib)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_isn(ip, port, count, iface, graph, verbose):

    conf.verb = False

    if iface:
        conf.iface = iface

    isn_values = []

    for _ in range(count):
        pkt = IP(dst=ip)/TCP(sport=RandShort(), dport=port, flags="S")
        ans = sr1(pkt, timeout=0.5)
        if ans:
            send(IP(dst=ip)/TCP(sport=pkt[TCP].sport, dport=port, ack=ans[TCP].seq + 1, flags='A'))
            isn_values.append(ans[TCP].seq)
            if verbose:
                ans.show2()

    if graph:

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("To graph support, install matplotlib")
            return 1

        plt.plot(range(len(isn_values)), isn_values, 'ro')
        plt.show()

    else:

        for v in isn_values:
            print(v)

    return True


if __name__ == '__main__':
    cmd_isn()

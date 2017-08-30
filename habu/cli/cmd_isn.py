import click
import matplotlib.pyplot as plt

from scapy.all import ICMP, IP, conf, sr1, UDP, TCP, srloop, send, RandShort
from time import sleep

@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-c', 'count', default=5, help='How many packets to send/receive (default: 5)')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_isn(ip, port, count, iface, verbose):

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
            ans.show2()
        #sleep(1)

    plt.plot(range(len(isn_values)), isn_values, 'ro')
    plt.show()

    #, count=count, verbose=verbose, inter=0.1)


    '''
    ans, unans = srloop(IP(dst=ip)/TCP(dport=port, flags="S"), count=count, verbose=verbose, inter=0.1)

    if verbose:
        for s,r in ans:
            print(r.summary())

    temp = 0
    isn_values = []

    for s,r in ans:
        temp = r[TCP].seq - temp
        print("%d\t%+d" %(r[TCP].seq, temp))
        isn_values.append(r[TCP].seq)

    plt.plot(range(len(isn_values)), isn_values, 'ro')
    plt.show()

    #plot_scatter(f=None, xs=range(len(isn_values)), ys=isn_values, size=100, pch='x', colour='#333', title='asd')
    '''

    return True


if __name__ == '__main__':
    cmd_isn()


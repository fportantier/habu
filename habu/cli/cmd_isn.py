import click
from scapy.all import ICMP, IP, conf, sr1, UDP, TCP, srloop


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

    ans, unans = srloop(IP(dst=ip)/TCP(dport=port, flags="S"), count=count, verbose=verbose, inter=0.1)

    if verbose:
        for s,r in ans:
            print(r.summary())

    temp = 0

    for s,r in ans:
        temp = r[TCP].seq - temp
        print("%d\t%+d" %(r[TCP].seq, temp))

    return True


if __name__ == '__main__':
    cmd_isn()


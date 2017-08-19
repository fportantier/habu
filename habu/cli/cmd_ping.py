import click
from scapy.all import ICMP, IP, conf, sr


@click.command()
@click.argument('ip')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_ping(ip, verbose):

    conf.verb = verbose

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

    pkts = layer3 / layer4

    count = len([ pkt for pkt in pkts ])
    print("Sending %d packets..." % count)

    ans, unans = sr(pkts, timeout=2)

    ans.summary()

    return True

if __name__ == '__main__':
    cmd_ping()

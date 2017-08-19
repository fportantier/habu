import click
from scapy.all import ICMP, IP, conf, sr, TCP


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_tcpflag(ip, port, verbose):

    conf.verb = verbose

    pkts = IP(dst=ip) / TCP(flags=(0, 255), dport=port)

    ans, unans = sr(pkts, timeout=2)

    out = "{:>8} -> {:<8}"

    for s,r in ans:
        print(out.format(s.sprintf(r"%TCP.flags%"), r.sprintf(r"%TCP.flags%")))

    return True

if __name__ == '__main__':
    cmd_tcpflag()


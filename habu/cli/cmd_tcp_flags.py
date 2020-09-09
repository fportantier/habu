#!/usr/bin/env python3

import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import IP, TCP, conf, sr1


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-f', 'flags', default=None, help='Flags that must be sent ever (default: fuzz with all flags)')
@click.option('-r', 'rflags', default=None, help='Filter by response flags (default: show all responses)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
@click.option('--first', 'first', is_flag=True, default=False, help='Stop on first response that matches')
def cmd_tcp_flags(ip, port, flags, rflags, verbose, first):
    """Send TCP packets with different flags and tell what responses receives.

    It can be used to analyze how the different TCP/IP stack implementations
    and configurations responds to packet with various flag combinations.

    Example:

    \b
    # habu.tcp_flags www.portantier.com
    S  -> SA
    FS -> SA
    FA -> R
    SA -> R

    By default, the command sends all possible flag combinations. You can
    specify which flags must ever be present (reducing the quantity of
    possible combinations), with the option '-f'.

    Also, you can specify which flags you want to be present on the response
    packets to show, with the option '-r'.

    With the next command, you see all the possible combinations that have
    the FIN (F) flag set and generates a response that contains the RST (R)
    flag.

    Example:

    \b
    # habu.tcp_flags -f F -r R www.portantier.com
    FPA  -> R
    FSPA -> R
    FAU  -> R
    """

    conf.verb = False

    pkts = [ (IP(dst=ip) / TCP(flags=f, dport=port)) for f in range(0, 512) ]

    out = "{:>8} -> {:<8}"

    for pkt in pkts:
        if not flags or all(i in pkt.sprintf(r"%TCP.flags%") for i in flags):
            if verbose:
                print(pkt.summary())
            ans = sr1(pkt, timeout=0.2)
            if ans:
                if not rflags or all(i in ans.sprintf(r"%TCP.flags%") for i in rflags):
                    print(out.format(pkt.sprintf(r"%TCP.flags%"), ans.sprintf(r"%TCP.flags%")))
                    if first:
                        break

    return True

if __name__ == '__main__':
    cmd_tcp_flags()

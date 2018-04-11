from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, conf, sr1

from habu.lib.firewall import Firewall


@click.command()
@click.option('--disable', is_flag=True, default=False, help='Disable firewalling')
@click.option('--no-rst', is_flag=True, default=False, help='Disable TCP RST output packets')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_firewall(disable, no_rst, verbose):

    fw = Firewall()

    if not any([disable, no_rst]):
        print("Nothing to do, use --help to see the available options.")

    if verbose:
        fw.verbose = verbose

    if disable:
        fw.disable()

    if no_rst:
        fw.no_rst()

    return True

if __name__ == '__main__':
    cmd_firewall()

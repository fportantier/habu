import click
import sys
import logging
from habu.lib.ip2asn import ip2asn
import json

@click.command()
@click.argument('ip')
def cmd_ip2asn(ip):

    data = ip2asn(ip)
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    cmd_ip2asn()


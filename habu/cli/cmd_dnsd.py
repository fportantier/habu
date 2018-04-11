import ipaddress
import json
import logging
import os
import pwd
import re
import sys
import time
from pathlib import Path

import click
from dnslib import QTYPE, RR, A
from dnslib.server import BaseResolver, DNSServer

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, conf, sr1

#logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

#from time import sleep


class MyResolver(BaseResolver):

    def __init__(self, addr4, addr6):
        self.address = address
        pass
        #user = pwd.getpwnam(sys.argv[1])

        #self.homedir = Path(user.pw_dir)
        #self.dotdir = self.homedir / '.asydns'
        #self.datadir = self.dotdir / 'data'

        #self.datadir.mkdir(parents=True, exist_ok=True)

        #self.regex_sha224 = re.compile('[0-9a-f]{56}')

        #self.cfg_file = self.dotdir / 'config.json'

        #defaults = {
        #    'domain': 'a.asydns.org',
        #    'ttl' : 3600,
        #    'registers': {}
        #}

        #self.cfg = defaults

        #if self.cfg_file.is_file():
        #    try:
        #        with self.cfg_file.open() as c:
        #            self.cfg.update(json.loads(c.read()))
        #    except Exception:
        #        print('error loading config file, using defaults', file=sys.stderr)


    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qn = str(qname)

        print(request.q)
        print(qname)


        #if qname in self.cfg['registers'].keys():
        answer = RR(qname, QTYPE.A, rdata=A(self.address), ttl=30)
        reply.add_answer(answer)

        #if self.regex_sha224.match(qn.split('.')[0]):
        #    sha224 = qn.split('.')[0]
        #    ip_file = self.datadir / sha224

        #    if ip_file.is_file() and (time.time() - ip_file.stat().st_mtime) < self.cfg['ttl']:
        #        with ip_file.open() as ipf:
        #            ip = ipf.read()
        #            answer = RR(qname, QTYPE.A, rdata=A(ip), ttl=30)
        #            reply.add_answer(answer)

        return reply


@click.command()
#@click.argument('ip')
@click.option('-i', 'iface', default=None, help='Interface to take addresses from')
@click.option('-4', 'ipv4', is_flag=True, default=False, help='Send IPv4 (A) responses')
@click.option('-6', 'ipv6', is_flag=True, default=False, help='Send IPv6 (AAAA) responses')
#@click.option('-t', 'timeout', default=2, help='Timeout in seconds (default: 2)')
#@click.option('-w', 'wait', default=1, help='How many seconds between packets (default: 1)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_dnsd(iface, ipv4, ipv6, verbose):

    if not ipv4 and not ipv6:
        print('You need to set at least one parameter -4 / -6')
        sys.exit(1)

    ifaces = { x[3] for x in conf.route.routes }
    ifaces = ifaces & { x[3] for x in conf.route6.routes }

    if not iface:
        iface = conf.iface

    if iface not in ifaces:
        print(iface, 'is an invalid iface, valid ifaces are: ', ifaces)
        sys.exit(1)

    if ipv4:
        addr4 = [x[4] for x in conf.route.routes if x[2] != '0.0.0.0' and x[3] == iface][0]
        if not addr4:
            print("IPv4 address not found")

    if ipv6:
        addr6 = [x[4] for x in conf.route6.routes if x[1] == 0 and x[3] == iface][0][-1]
        if not addr6:
            print("IPv6 address not found")

    print(addr4)
    print(addr6)

    sys.exit(0)

    resolver = MyResolver(addr4=addr4, addr6=addr6)

    server = DNSServer(
        resolver,
        port=53,
        address="0.0.0.0"
    )

    server.start_thread()
    #drop_privileges(sys.argv[1])

    while server.isAlive():
        time.sleep(1)


    return True

if __name__ == '__main__':
    cmd_dnsd()

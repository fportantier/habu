"""Retrieve details about a domain."""
import logging
import sys

import click

from habu.lib.dns import _query as query


@click.command()
@click.argument('ip_address')
@click.option('-v', 'verbose', is_flag=True, default=False,
              help='Verbose output.')
@click.option('-n', 'name_server', default='8.8.8.8',
              help='Nameserver to use.')
def cmd_dns_query(ip_address, name_server, verbose):
    """Retrieve details about a domain.

    Example:

    \b
    $ habu.dns.server google.com
    id 11316
    opcode QUERY
    rcode NOERROR
    flags QR RD RA
    edns 0
    payload 512
    ;QUESTION
    google.com. IN ANY
    ;ANSWER
    google.com. 299 IN A 172.217.22.14
    google.com. 299 IN AAAA 2a00:1450:4001:81a::200e
    google.com. 21599 IN CAA 0 issue "pki.goog"
    google.com. 599 IN MX 50 alt4.aspmx.l.google.com.
    google.com. 599 IN MX 20 alt1.aspmx.l.google.com.
    google.com. 599 IN MX 30 alt2.aspmx.l.google.com.
    google.com. 599 IN MX 10 aspmx.l.google.com.
    google.com. 599 IN MX 40 alt3.aspmx.l.google.com.
    google.com. 21599 IN NS ns1.google.com.
    google.com. 21599 IN NS ns4.google.com.
    google.com. 21599 IN NS ns2.google.com.
    google.com. 21599 IN NS ns3.google.com.
    google.com. 299 IN TXT "v=spf1 include:_spf.google.com ~all"
    google.com. 299 IN TXT "globalsign-smime-dv=CDYX+XF....vqKX8="
    google.com. 299 IN TXT "facebook-domain-verification=22rm55....4h95"
    google.com. 299 IN TXT "docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e"
    google.com. 59 IN SOA ns1.google.com. dns-admin.google.com. 244037683 900 900 1800 60
    ;AUTHORITY
    ;ADDITIONAL
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        print("Looking up %s..." % ip_address, file=sys.stderr)

    result = query(ip_address, name_server)

    if result:
        print(result)
    else:
        print("[X] Unable to retrieve data for %s" % ip_address)

    return True


if __name__ == '__main__':
    cmd_dns_query()

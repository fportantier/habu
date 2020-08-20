#!/usr/bin/env python3

import json
import logging

import dns.query
import dns.resolver
import dns.zone

import click

from habu.lib import dnsx
from habu.lib.fqdn_finder import fqdns_from_ct_log, fqdns_from_hosts, fqdns_from_brute_force, fqdns_from_weblinks


@click.command()
@click.option('-t', 'timeout', type=click.FLOAT, default=1, help='Time to wait for each connection')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--debug', 'debug', is_flag=True, default=False, help='Debug output')
@click.option('--connect/--no-connect', 'connect', default=True, help='Get from known FQDNs open ports SSL certificates')
@click.option('--brute/--no-brute', 'brute_force', default=True, help='Run DNS brute force against domains')
@click.option('--links/--no-links', 'weblinks', default=True, help='Extract FQDNs from web site links')
@click.option('--xfr/--no-xfr', 'xfr', default=True, help='Try to do a DNS zone transfer against domains')
@click.option('--ctlog/--no-ctlog', 'ctlog', default=True, help='Try to get FQDNs from Certificate Transparency Logs')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
@click.argument('domains', nargs=-1)
def cmd_fqdn_finder(domains, brute_force, connect, xfr, ctlog, weblinks, timeout, verbose, debug, json_output):
    """
    Uses various techniques to obtain valid FQDNs for the specified domains.

    \b
    1. Try to all FQDNs with DNS zone transfers
    2. Check for Certificate Transparency Logs
    3. Connect to specified ports, obtain SSL certificates and get FQDNs from them
    4. Connect to websites and get FQDNs based on the website links
    5. DNS Brute Force for common names

    The results are cleaned to remove FQDNs that does not resolve by DNS

    Example:

    \b
    $ habu.fqdn.finder educacionit.com
    barometrosalarial.educacionit.com
    blog.educacionit.com
    ci.educacionit.com
    educacionit.com
    intranet.educacionit.com
    lecdev.educacionit.com
    lecweb.educacionit.com
    mail.educacionit.com
    plantillas.educacionit.com
    www.educacionit.com
    """

    domains = set(domains)
    #print(domains)

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    fqdns = set()

    if xfr:
        logging.info('Trying to get DNS Zones with a Zone Transfer..')
        for domain in list(domains):
            for ns_server in dnsx.ns(domain):
                try:
                    z = dns.zone.from_xfr(dns.query.xfr(ns_server, domain, lifetime=5))
                except Exception as e:
                    z = None
                if z:
                    logging.info('Got DNS Zone with XFR for {} domain'.format(domain))
                    domains.remove(domain) # it's safe to remove the domains if zone available via XFR?
                    for name in z.nodes.keys():
                        fqdns.add(str(name) + '.' + domain)
                    break

    if ctlog:
        for domain in domains:
            logging.info('Getting FQDNs for {} from certificate transparency logs...'.format(domain))
            result = fqdns_from_ct_log(domain)
            logging.info('Got {} FQDNs'.format(len(result)))
            fqdns |= result

    logging.info('Removing FQDNs that does not resolve by DNS...')
    for fqdn in list(fqdns):
        if not dnsx.resolve(fqdn):
            logging.info('Removing {} because does not resolves by DNS'.format(fqdn))
            fqdns.remove(fqdn)

    if connect:
        logging.info('Getting FQDNs from SSL certificates')
        result = fqdns_from_hosts(fqdns, domains=domains)
        logging.info('Got {} FQDNs'.format(len(result)))
        fqdns |= result

    if weblinks:
        logging.info('Getting FQDNs from web links')
        for fqdn in list(fqdns):
            result = fqdns_from_weblinks(fqdn, domains=domains)
            logging.info('Got {} FQDNs'.format(len(result)))
            fqdns |= result

    if brute_force:
        logging.info('Running DNS brute force...')
        for domain in domains:
            result = fqdns_from_brute_force(domain)
            logging.info('Got {} FQDNs'.format(len(result)))
            fqdns |= result

    if json_output:
        print(json.dumps(sorted(fqdns), indent=4))
    else:
        print('\n'.join(sorted(fqdns)))


if __name__ == '__main__':
    cmd_fqdn_finder()

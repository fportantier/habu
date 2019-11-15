#!/usr/bin/env python3

import json
import logging

import click

from habu.lib import libdns
from habu.lib.fqdn_finder import fqdns_from_ct_log, fqdns_from_hosts


@click.command()
@click.option('-p', 'ports', default='443', help='Ports to connect to check for SSL certificates (comma separated list)')
@click.option('-t', 'timeout', type=click.FLOAT, default=1, help='Time to wait for each connection')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
@click.argument('domains', nargs=-1)
def cmd_fqdn_finder(domains, ports, timeout, verbose, json_output):
    """
    Uses various techniques to obtain valid FQDNs for the specified domains.

    1. Check for Certificate Transparency Logs ()
    2. Connect to specified ports, obtain SSL certificates and get FQDNs from them

    Next versions will also do the following:

    3. DNS Brute Force for common names
    4. Try DNS Zone Transfer first

    The results are cleaned to remove FQDNs that does not resolve by DNS

    Example:

    \b
    $ habu.fqdn.finder educacionit.com
    azure-001.educacionit.com
    barometrosalarial.educacionit.com
    blog.educacionit.com
    blog2.educacionit.com
    ci.educacionit.com
    educacionit.com
    freelancerday.educacionit.com
    intranet.educacionit.com
    lecdev.educacionit.com
    lecdev2.educacionit.com
    lecweb.educacionit.com
    live.educacionit.com
    mail.educacionit.com
    noticias.educacionit.com
    plantillas.educacionit.com
    talentos.educacionit.com
    tsg-001.educacionit.com
    vmm-001.educacionit.com
    www.barometrosalarial.educacionit.com
    www.educacionit.com
    www.intranet.educacionit.com
    www.noticias.educacionit.com
    www.plantillas.educacionit.com
    www.talentos.educacionit.com
    """

    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    fqdns = set()

    for domain in domains:
        logging.info('Getting FQDNs for {} from certificate transparency logs...'.format(domain))
        fqdns |= fqdns_from_ct_log(domain)

    logging.info('Removing FQDNs that does not resolve by DNS...')
    for fqdn in list(fqdns):
        if not libdns.resolve(fqdn):
            logging.info('Removing {} because does not resolves by DNS'.format(fqdn))
            fqdns.remove(fqdn)

    logging.info('Getting FQDNs from SSL certificates on host ports {}'.format(','.join(ports)))
    fqdns |= fqdns_from_hosts(fqdns, domains=domains, ports=[443])

    if json_output:
        print(json.dumps(sorted(fqdns), indent=4))
    else:
        print('\n'.join(sorted(fqdns)))


if __name__ == '__main__':
    cmd_fqdn_finder()

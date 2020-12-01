#!/usr/bin/env python3

import ipaddress
import json
import logging
import os
import os.path
import socket
import ssl
import sys
from pathlib import Path
from time import sleep

import dns.resolver
import dns.zone
import requests
import requests_cache
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import NameOID
import tldextract

from habu.lib.shodan import shodan_get_result
from habu.lib.tomorrow3 import threads
from habu.lib import dnsx
from habu.lib.loadcfg import loadcfg
from habu.lib.web_links import web_links


config = loadcfg()

def fqdns_from_ct_log(domain, cache=True, verbose=False):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if cache:
        homedir = Path(os.path.expanduser('~'))
        requests_cache.install_cache(str((homedir / '.habu_requests_cache')), expire_after=3600)

    fqdns = set()

    if verbose:
        print("Downloading subdomain list from https://crt.sh ...", file=sys.stderr)

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=domain))

    if req.status_code != 200:
        print("[X] Information not available!")
        return False

    json_data = json.loads(req.text)

    for data in json_data:
        names = data['name_value'].lower().split('\n')
        for name in names:
            if name and '*' not in name:
                fqdns.add(name)

    return fqdns


def fqdns_from_certificate(cert_data):

    try:
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    except ValueError:
        pass

    try:
        cert = x509.load_der_x509_certificate(cert_data, default_backend())
    except ValueError:
        raise ValueError("No recognized cert format. Allowed: PEM or DER")

    names = set()
    names.add(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value.lower().rstrip('.'))

    try:
        alt_names = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    except x509.extensions.ExtensionNotFound:
        alt_names = None

    if alt_names:
        for alt_name in alt_names.value.get_values_for_type(x509.DNSName):
            names.add(alt_name.lower().rstrip('.'))

    return list(sorted(names))



def fqdns_from_hosts(hosts, domains, timeout=2):

    result = set()

    addrs = {}

    for host in list(hosts):
        resolves_to = dnsx.resolve(host)
        if resolves_to:
            for addr in resolves_to:
                addrs[addr] = set(addrs.get(addr, [])) | set(host)

    for addr, fqdns in addrs.items():

        shodan_result = shodan_get_result(addr)

        if not shodan_result:
            continue

        for port in shodan_result['data']:

            if port['transport'] != 'tcp':
                continue

            if 'ssl' not in port:
                continue

            logging.info('connecting to {}:{}'.format(addr, port['port']))

            for fqdn in fqdns:

                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                try:
                    with socket.create_connection((str(addr), int(port['port'])), timeout=timeout) as sock:
                        with context.wrap_socket(sock) as ssock:
                            cert = ssock.getpeercert(binary_form=True)
                            fqdns_in_cert = set(fqdns_from_certificate(cert))
                            logging.debug('obtained fqdns: {}'.format(', '.join(fqdns_in_cert)))
                            result |= fqdns_in_cert
                except Exception as e:
                    break

    # Remove FQDNs that are not in any of the domains
    for fqdn in list(result):
        if not any([fqdn.endswith(domain) for domain in domains]):
            result.remove(fqdn)

    return result



@threads(20)
def dns_query(hostname):
    try:
        answer = dns.resolver.query(hostname)
        return answer
    except Exception:
        return None


def fqdns_from_brute_force(domain):

    fqdns = set()
    nxdomain = None

    try:
        nxdomain = dns.resolver.query('nonexistent456789.' + domain)
    except dns.resolver.NXDOMAIN:
        nxdomain = None

    with (config['DATADIR'] / 'subdomains.txt').open() as subdomains_file:
        subdomains_txt = subdomains_file.read()

    subdomains = { s + '.' + domain for s in subdomains_txt.split('\n') }

    subdomains.add(domain)

    jobs = [dns_query(sd) for sd in subdomains ]

    while True:
        if any([ job.running() for job in jobs]):
            sleep(1)
        else:
            break

    for job in jobs:

        result = job.result()

        if not hasattr(result, 'rrset'):
            continue

        if nxdomain and nxdomain.rrset[0] == result.rrset[0]:
            continue

        if str(result.rrset[0]).startswith('127.'):
            continue

        for r in result.rrset:
            fqdns.add(str(result.qname).rstrip('.'))

    return fqdns


def fqdns_from_weblinks(hostname, domains, timeout=5):

    fqdns = set()

    addrs = dnsx.resolve(hostname)

    if not addrs:
        return fqdns

    addr = addrs[0]

    shodan_result = shodan_get_result(addr)

    if not shodan_result:
        return fqdns

    for port in shodan_result['data']:

        if 'http' not in port:
            continue

        if 'ssl' in port:
            scheme = 'https'
        else:
            scheme = 'http'

        url = '{}://{}:{}'.format(scheme, hostname, port['port'])

        logging.info('connecting to {}'.format(url))

        links = web_links(url)

        for link in links:
            tld = tldextract.extract(link)
            domain = '{}.{}'.format(tld.domain, tld.suffix)
            if domain in domains:
                if tld.subdomain:
                    fqdns.add('{}.{}.{}'.format(tld.subdomain, tld.domain, tld.suffix))

    return fqdns



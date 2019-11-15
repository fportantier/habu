#!/usr/bin/env python3

import json
import logging
import os
import os.path
import socket
import ssl
import sys
from pathlib import Path

import requests
import requests_cache
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import NameOID

from habu.lib import libdns


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
        name = data['name_value'].lower()
        if '*' not in name:
            fqdns.add(name)

    return fqdns

    '''
    subdomains = list(subdomains)

    if no_validate:
        print(json.dumps(sorted(subdomains), indent=4))
        return True

    if verbose:
        print("Validating subdomains against DNS servers ...", file=sys.stderr)

    answers = query_bulk(subdomains)

    validated = []

    for answer in answers:
        if answer:
            validated.append(str(answer.qname))

    print(json.dumps(sorted(validated), indent=4))
    return True
    '''

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
    names.add(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value.lower())

    try:
        alt_names = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    except x509.extensions.ExtensionNotFound:
        alt_names = None

    if alt_names:
        for alt_name in alt_names.value.get_values_for_type(x509.DNSName):
            names.add(alt_name.lower())

    return list(sorted(names))



def fqdns_from_hosts(hosts, domains, ports=[443], timeout=2):

    result = set()

    addrs = {} # host : [] for host in hosts }

    for host in list(hosts):
        resolves_to = libdns.resolve(host)
        if resolves_to:
            for addr in resolves_to:
                addrs[addr] = set(addrs.get(addr, [])) | set(host)
        #else:
        #    del hosts[host]

    for addr, fqdns in addrs.items():

        for port in ports:

            for fqdn in fqdns:

                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                try:
                    with socket.create_connection((str(addr), int(port)), timeout=timeout) as sock:
                        with context.wrap_socket(sock) as ssock:
                            cert = ssock.getpeercert(binary_form=True)
                            result |= set(fqdns_from_certificate(cert))
                            #all_names |= set(names)
                            #print(' '.join(names))
                except Exception as e:
                    #print(e)
                    break

    # Remove FQDNs that are not in any of the domains
    for fqdn in list(result):
        if not any([fqdn.endswith(domain) for domain in domains]):
            result.remove(fqdn)

    return result



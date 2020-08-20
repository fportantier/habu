#!/usr/bin/env python3

import ipaddress
import socket
from time import sleep

import dns.resolver
import dns.zone
import dns

from dns import resolver, reversename

from habu.lib.tomorrow3 import threads


def resolve(name, server=None):
    """resolves the name"""

    my_resolver = dns.resolver.Resolver()

    if server:
        my_resolver.nameservers = [server]

    result = []

    try:
        answers = my_resolver.resolve(str(name), lifetime=3)
    except Exception as e:
        answers = []

    answers = [ str(answer) for answer in answers ]

    return answers


def ns(domain):
    """returns a list with the NS servers for domain"""

    result = []

    try:
        answers = dns.resolver.resolve(domain, 'NS')
    except Exception:
        answers = []

    for rdata in answers:
        result.append(str(rdata.target).lower())

    return result


def mx(domain):
    """returns a list with the MX servers for domain"""

    result = []

    try:
        answers = dns.resolver.resolve(domain, 'MX')
    except Exception:
        answers = []

    for rdata in answers:
        result.append(str(rdata.exchange).lower())

    return result


def axfr(domain):
    """ returns a list with the ns that allows zone transfers"""

    allowed = []

    for server in ns(domain):

        server_ip = resolve(server)

        if not server_ip:
            continue

        try:
            z = dns.zone.from_xfr(dns.query.xfr(server_ip[0], domain))
            if z.nodes.keys():
                allowed.append(server)
        except Exception as e:
            pass

    return allowed


@threads(50)
def __threaded_query(hostname):
    """Perform the requests to the DNS server."""
    try:
        answer = resolver.resolve(hostname)
        return answer
    except Exception:
        return None


def query_bulk(names):
    """Query server with multiple entries."""
    answers = [__threaded_query(name) for name in names]

    while True:
        if all([a.done() for a in answers]):
            break
        sleep(1)

    return [answer.result() for answer in answers]


def lookup_reverse(ip_address):
    """Perform a reverse lookup of IP address."""
    try:
        type(ipaddress.ip_address(ip_address))
    except ValueError:
        return {}

    record = reversename.from_address(ip_address)
    hostname = str(resolver.resolve(record, "PTR")[0])[:-1]
    return {'hostname': hostname}


def lookup_forward(name):
    """Perform a forward lookup of a hostname."""
    ip_addresses = {}

    addresses = list(set(str(ip[4][0]) for ip in socket.getaddrinfo(
        name, None)))

    if addresses is None:
        return ip_addresses

    for address in addresses:
        if type(ipaddress.ip_address(address)) is ipaddress.IPv4Address:
            ip_addresses['ipv4'] = address
        if type(ipaddress.ip_address(address)) is ipaddress.IPv6Address:
            ip_addresses['ipv6'] = address

    return ip_addresses


if __name__ == '__main__':
    print(ns('securetia.com'))
    print(mx('securetia.com'))
    print(axfr('securetia.com'))

import ipaddress
import socket
from time import sleep

from dns import resolver, reversename

from habu.lib.tomorrow3 import threads


@threads(50)
def __threaded_query(hostname):
    """Perform the requests to the DNS server."""
    try:
        answer = resolver.query(hostname)
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
    hostname = str(resolver.query(record, "PTR")[0])[:-1]
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

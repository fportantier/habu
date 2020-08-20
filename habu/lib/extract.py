import ipaddress
from collections import OrderedDict

import tldextract
import validators


def valid_domain(item):

    if validators.domain(item) is not True:
        return False

    x = tldextract.extract(item)
    return x.subdomain is ''


def valid_fqdn(item):

    if validators.domain(item) is not True:
        return False

    x = tldextract.extract(item)
    return x.subdomain is not ''


def valid_ipv4_address(item):

    try:
        ipaddress.IPv4Address(item)
        return True
    except ValueError:
        return False


def valid_ipv4_network(item):

    try:
        ipaddress.IPv4Network(item)
        return True
    except ValueError:
        return False


def valid_ipv6_address(item):

    try:
        ipaddress.IPv6Address(item)
        return True
    except ValueError:
        return False


def valid_ipv6_network(item):

    try:
        ipaddress.IPv6Network(item)
        return True
    except ValueError:
        return False


validator_functions = OrderedDict()
validator_functions['ipv4_address'] = valid_ipv4_address
validator_functions['ipv4_network'] = valid_ipv4_network
validator_functions['ipv6_address'] = valid_ipv6_address
validator_functions['ipv6_network'] = valid_ipv6_network
validator_functions['url'] = validators.url
validator_functions['fqdn'] = valid_fqdn
validator_functions['domain'] = valid_domain
validator_functions['email'] = validators.email
validator_functions['mac_address'] = validators.mac_address
validator_functions['md5'] = validators.md5
validator_functions['sha1'] = validators.sha1
validator_functions['sha224'] = validators.sha224
validator_functions['sha256'] = validators.sha256
validator_functions['sha512'] = validators.sha512
validator_functions['pan'] = validators.card.card_number


def guess_item_type(item):
    for item_type, function in validator_functions.items():
        if function(item):
            return item_type
    return None

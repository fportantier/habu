import ipaddress

from habu.lib.identify import identify
from habu.lib.ip2asn import ip2asn

def expand_ip(addr):

    result = {}

    ip = ipaddress.ip_network(addr, strict=False)

    prop_host = [ 'version', 'is_multicast', 'is_global', 'is_unspecified', 'is_reserved', 'is_loopback', 'is_link_local' ]

    prop_network = [ 'prefixlen', 'netmask', 'network_address', 'broadcast_address', 'num_addresses' ]

    for prop in prop_host:
        result[prop] = getattr(ip, prop)

    if ip.num_addresses > 1:
        for prop in prop_network:
            result[prop] = getattr(ip, prop)

    return result


expanders = {}
expanders['IPAddress'] = []
expanders['IPNetwork'] = []
expanders['Unknown'] = []
#expanders['IPAddress'].append(ip2asn)
expanders['IPAddress'].append(expand_ip)
expanders['IPNetwork'].append(expand_ip)


def expand(asset):

    family = identify(asset)

    result = {
        'asset': asset,
        'family' : family,
    }

    for expander in expanders[family]:
        result.update(expander(asset))

    return result



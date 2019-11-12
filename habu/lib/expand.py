import ipaddress

from habu.lib.identify import identify
from habu.lib.extract import guess_item_type

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
expanders['ipv4_address'] = []
expanders['ipv4_network'] = []
expanders['ipv6_address'] = []
expanders['ipv6_network'] = []
expanders['unknown'] = []
#expanders['IPAddress'].append(ip2asn)
expanders['ipv4_address'].append(expand_ip)
expanders['ipv4_network'].append(expand_ip)
expanders['ipv6_address'].append(expand_ip)
expanders['ipv6_network'].append(expand_ip)



def expand(item):

    family = guess_item_type(item)

    result = {
        'item': item,
        'family' : family,
    }

    for expander in expanders[family]:
        result.update(expander(item))

    return result



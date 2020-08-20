import ipaddress

from habu.lib.extract import guess_item_type

from habu.lib.ip2asn import ip2asn

def enrich_ip(addr):

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


enrichers = {}
enrichers['domain'] = []
enrichers['hostname'] = []
enrichers['ipv4_address'] = []
enrichers['ipv4_network'] = []
enrichers['ipv6_address'] = []
enrichers['ipv6_network'] = []
enrichers['unknown'] = []
#enrichers['IPAddress'].append(ip2asn)
enrichers['ipv4_address'].append(enrich_ip)
enrichers['ipv4_network'].append(enrich_ip)
enrichers['ipv6_address'].append(enrich_ip)
enrichers['ipv6_network'].append(enrich_ip)



def enrich(item):

    family = guess_item_type(item)

    result = {
        'item': item,
        'family' : family,
    }

    for enricher in enrichers[family]:
        result.update(enricher(item))

    return result



import ipaddress
import dns


def is_ipaddress(item):
    try:
        ipaddress.ip_address(item)
        return True
    except Exception:
        return False


def is_ipnetwork(item):
    try:
        ipaddress.ip_network(item)
        return True
    except Exception:
        return False


def is_domain(item):
    dns.name.from_text(item)



# We need to do more work on this function, because can fail on a lot of circumstances
def item_type(item):

    if item.startswith('http://') or item.startswith('https://'):
        return ['web']

    if '@' in item:
        return ['email']

        pass
    try:
        ipaddress.ip_network(item)
        return ['network']
    except Exception:
        pass

    # Si tiene servidores NS asociados, es un dominio o subdominio


    if habu.lib.dns.ns(item):
        return ['domain']

    # Si resuelve por DNS, es un hostname
    if habu.lib.dns.resolve(item):
        return ['fqdn']

    # Si no, no sabemos qué es.
    return None



if __name__ == '__main__':

    test_items = [
        'asd@asd.com',
        'microsoft.com',
        'invalid!domain.com',
        '8.8.8.8',
        '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        '8.8.8.0/24',
        'www.microsoft.com',
    ]

    for item in test_items:
        print(item, item_type(item))



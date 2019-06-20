import ipaddress

def identify(asset):

    try:
        ipaddress.ip_address(asset)
        return 'IPAddress'
    except Exception:
        pass
    try:
        ipaddress.ip_network(asset)
        return 'IPNetwork'
    except Exception:
        pass

    return 'Unknown'

    '''
    if asset.startswith('http://') or asset.startswith('https://'):
        return 'web'
    if '@' in asset:
        return 'email'
    # Si tiene servidores NS asociados, es un dominio o subdominio
    if libdns.ns(asset):
        return 'domain'

    # Si resuelve por DNS, es un hostname
    if libdns.resolve(asset):
        return 'hostname'

    # Si no, no sabemos qué es.
    return None
    '''


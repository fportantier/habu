import sys
from scapy.all import conf, get_if_hwaddr


if sys.platform.startswith('win'):
    from scapy.all import get_windows_if_list
    interfaces = get_windows_if_list()
    windows = True
else:
    from scapy.all import get_if_list
    interfaces = get_if_list()
    windows = False


def get_ifaces():
    """Get a list of network interfces.
    Returns a list like this:

    {'eth0': {'index': 0,
              'inet': None,
              'inet6': None,
              'mac': '80:fa:5b:4b:f9:18',
              'name': 'eth0'},
     'lo': {'index': 1,
            'inet': '127.0.0.1',
            'inet6': '::1',
            'mac': '00:00:00:00:00:00',
            'name': 'lo'},
     'vboxnet0': {'index': 3,
                  'inet': '192.168.56.1',
                  'inet6': 'fe80::800:27ff:fe00:0',
                  'mac': '0a:00:27:00:00:00',
                  'name': 'vboxnet0'},
     'wlan0': {'index': 2,
               'inet': '192.168.0.6',
               'inet6': None,
               'mac': 'f4:96:34:e5:ae:1b',
               'name': 'wlan0'}}
    """

    result = {}
    index = 0

    for i in interfaces:
        # Unix return strings and Windows dictionaries
        if isinstance(i, str):
            name = i
        elif isinstance(i, dict):
            name = i['name']
        else:
            print('Unexpected result', file=sys.stderr)
            return {}

        result[name] = { 'name' : name, 'index' : index }
        if windows:
            result[name]['mac'] = i['mac']
        else:
            result[name]['mac'] = get_if_hwaddr(name)

        if not result[name]['mac']:
            result[name]['mac'] = None

        result[name]['inet'] = None
        for route in conf.route.routes:
            if getattr(route[3], 'name', route[3]) == name:
                result[name]['inet'] = route[4]
                break

        result[name]['inet6'] = None
        for route in conf.route6.routes:
            if getattr(route[3], 'name', route[3]) == name:
                result[name]['inet6'] = route[4][0]
                break

        index += 1

    return result


def search_iface(term):
    """Get a valid interface based on a search term, that can be:
    The interface name
    The interface index - This is NOT the Windows Interface Index
    The interface inet address
    The interface inet6 address
    The interface mac address"""

    if not term:
        return None

    for iface in get_ifaces().values():
        if term in iface.values():
            return iface

        if str(term) == str(iface['index']):
            return iface

    return None


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ifaces())

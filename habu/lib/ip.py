"""Handle the inquests around IP addresses."""
import ipaddress

import requests


def get_ip():
    """Get the external IP address for the connection."""
    ip_address = requests.get('https://api.ipify.org', timeout=5).text
    return {'ip_external': ip_address}


def geo_location(ip_address):
    """Get the Geolocation of an IP address."""
    try:
        type(ipaddress.ip_address(ip_address))
    except ValueError:
        return {}

    data = requests.get(
        'https://ipapi.co/{}/json/'.format(ip_address), timeout=5).json()
    return data


if __name__ == '__main__':
    print(get_ip())

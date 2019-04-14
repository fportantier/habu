import requests


def get_ip():
    """Get the external IP address for the connection."""
    ip_address = requests.get('https://api.ipify.org', timeout=5).text
    return {'ip_external': ip_address}


if __name__ == '__main__':
    print(get_ip())

import requests


def get_ip():
    return requests.get('https://api.ipify.org').text

if __name__ == '__main__':
    print(get_ip())

import requests
import socket

socket.setdefaulttimeout(1)


def check_dns(hostnames=['www.google.com', 'www.microsoft.com']):
    for hostname in hostnames:
        try:
            socket.gethostbyname(hostname)
            return True
        except Exception:
            pass

    return False


def check_http(urls=['http://www.google.com', 'http://www.microsoft.com']):
    for url in urls:
        try:
            requests.get(url, timeout=1)
            return True
        except Exception:
            pass

    return False


def check_https(urls=['https://www.google.com', 'https://www.microsoft.com']):
    for url in urls:
        try:
            requests.get(url, timeout=1)
            return True
        except Exception:
            pass

    return False


def check_ftp(servers=['ftp.debian.org', 'ftp.redhat.com']):
    for server in servers:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server, 21))
            return True
        except Exception:
            pass

    return False


def check_ssh(servers=['www.github.com', 'www.gitlab.com']):
    for server in servers:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server, 22))
            return True
        except Exception:
            pass

    return False


if __name__ == '__main__':
    print(check_dns())
    print(check_ftp())
    print(check_http())
    print(check_https())


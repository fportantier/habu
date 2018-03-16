import requests
import socket

dns_servers = ['8.8.8.8', '8.8.4.4']
ftp_servers = ['ftp.debian.org', 'ftp.redhat.com']
http_servers = ['www.google.com', 'www.ibm.com']
ssh_servers = ['www.github.com']

socket.setdefaulttimeout(2)

def check_ip():
    for server in dns_servers:
        try:
            socket.create_connection((server, 53), 5)
            return True
        except socket.timeout:
            pass

    return False


def check_dns():
    for server in http_servers:
        try:
            socket.gethostbyname(server)
            return True
        except Exception:
            pass

    return False


def check_http():
    for server in http_servers:
        try:
            requests.get('http://' + server)
            return True
        except Exception:
            pass

    return False


def check_https():
    for server in http_servers:
        try:
            requests.get('https://' + server)
            return True
        except Exception:
            pass

    return False


def check_ftp():
    for server in ftp_servers:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server, 21))
            return True
        except Exception:
            pass

    return False


def check_ssh():
    for server in ssh_servers:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('sdf.org', 22))
            return True
        except Exception:
            pass

    return False


if __name__ == '__main__':
    print(check_ip())
    print(check_dns())
    print(check_ftp())
    print(check_http())
    print(check_https())


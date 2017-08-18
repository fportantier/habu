from scapy.all import *
from pprint import pprint

def pscan_tcp_syn(ip, ports=[80]):

    result = { p:'closed' for p in ports }

    ans,unans = sr(IP(dst=ip)/TCP(sport=RandShort(), dport=ports, flags='S'), timeout=2, verbose=False)

    for pkt in ans:
        if pkt[1]['TCP'].flags == 18: # 18 = SA
            result[pkt[1]['TCP'].sport] = 'open'

    return result


def pscan_tcp_fin(ip, ports=[80]):

    result = { p:'open' for p in ports }

    ans,unans = sr(IP(dst=ip)/TCP(sport=RandShort(), dport=ports, flags='F'), timeout=2, verbose=False)

    print(ans.summary(), unans.summary())

    for pkt in ans:
        if pkt[1]['TCP'].flags == 18: # 18 = SA
            result[pkt[1]['TCP'].sport] = 'open'

    return result


if __name__ == '__main__':
    #print(pscan_tcp_syn('www.google.com', [22, 80]))
    print(pscan_tcp_fin('www.redhat.com', [22, 80]))



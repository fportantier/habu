import click

help_text = [
    ('habu.arpoison', 'ARP cache poisoner *'),
    ('habu.arping', 'ARP ping *'),
    ('habu.arpsniff', 'ARP sniffer *'),
    ('habu.b64', 'Base 64 encoder / decoder'),
    ('habu.contest', 'Check internet connection capabilities'),
    ('habu.dhcp_discover', 'Find DHCP servers on local network'),
    ('habu.dhcp_starvation', 'DHCP starvation attack'),
    ('habu.eicar', 'Print the EICAR test string'),
    ('habu.forkbomb', 'Show various forkbomb examples'),
    ('habu.hasher', 'Calculate hashes using various algorithms'),
    ('habu.help', 'Print this help message'),
    ('habu.ip', 'Show your public IP'),
    ('habu.ip2asn', 'IP2ASN and another IP data'),
    ('habu.isn', 'TCP ISN analyzer'),
    ('habu.karma', 'Check an IP against a lot of Threat Intelligence lists'),
    ('habu.land', 'LAND attack'),
    ('habu.ping', 'Simple ICMP ping'),
    ('habu.snmp_crack', 'Simple SNMP brute forcer'),
    ('habu.synflood', 'SYN Flood attack'),
    ('habu.tcpflags', 'TCP flags analyzer'),
    ('habu.tcpscan', 'Simple TCP port scanner'),
    ('habu.traceroute', 'Simple traceroute'),
    ('habu.webid', 'Web technologies identificator'),
    ('habu.xor', 'XOR cipher'),
]

@click.command()
def cmd_help():
    """Habu help"""

    print('* = Need root privileges')

    for c, h in help_text:
        print('%-20s%-12s' % (c, h))

if __name__ == '__main__':
    cmd_help()

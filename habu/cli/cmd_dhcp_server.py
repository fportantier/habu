import click
from scapy.all import ICMP, IP, conf, sr1, UDP, TCP, Ether, BOOTP, DHCP, get_if_raw_hwaddr, RandMAC, srp, DHCP_am
from time import sleep

@click.command()
@click.option('-i', 'iface', default=None, help='Interface to use')
#@click.option('-g', 'gateway', default=None, help='Gateway (default: interface address)')
#@click.option('-d', 'dns', default=None, help='DNS (default: interface address)')
#@click.option('-p', 'pool', default=None, help='Address pool (default: interface network)')
#@click.option('-m', 'mask', default=None, help='Network mask (default: interface network mask)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_dhcp_server(iface, verbose):

    conf.verb = False

    if iface:
        conf.iface = iface

    #print(conf)

    '''
    dhcp_server = DHCP_am(
                            iface=conf.iface,
                            domain='example.com',
                            pool=Net('192.168.10.0/24'),
                            network='192.168.10.0/24',
                            gw='192.168.10.254',
                            renewal_time=600, lease_time=3600
                        )
    dhcp_server()
    '''
    print(conf.route)

if __name__ == '__main__':
    cmd_dhcp_server()


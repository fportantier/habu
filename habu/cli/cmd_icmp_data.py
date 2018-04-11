from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *


@click.command()
#@click.option('-i', 'iface', default=None, help='Interface to use')
#@click.option('-t', 'timeout', default=1, help='Time (seconds) to wait for responses')
@click.option('-s', 'src', default=None, help='Show only packets from source')
@click.option('-d', 'dst', default=None, help='Show only packets from destination')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_icmp_data(src, dst, verbose):

    data = b""

    conf.verb = False

    # rdpcap comes from scapy and loads in our pcap file
    packets = rdpcap('/home/f/Downloads/ch6.pcap')

    # Let's iterate through every packet
    for packet in packets:
        if ICMP in packet:
            if not src or packet[IP].src == src:
                if not dst or packet[IP].dst == dst:
                    #print(packet[Raw].load)
                    data += packet[Raw].load
                    #packet.show()
                    #print(packet)

    with open('out', 'wb') as out:
        out.write(data)

    print(data)
    print(data.decode(errors='ignore'))

if __name__ == '__main__':
    cmd_icmp_data()

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ICMP, IP, TCP, conf, icmpcodes, sr, sr1


@click.command()
@click.argument('ip')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_icmp(ip, verbose):

    conf.verb = False

    #pkts = IP(dst=ip) / TCP(flags=(0, 255), dport=port)
    pkt = IP(dst=ip) / ICMP()# , proto=(0, 255)) # / TCP(flags=(0, 255), dport=port)


    messages = [
        (8, 0),  # echo request
        (13, 0), # timestamp
        (15, 0), # info request
        #(), #
        #(), #
    ]

    #print(pkts.summary())
    #print(pkts.show2())

    #print(icmpcodes)

    for itype, icode in messages:
        pkt[ICMP].type = itype
        pkt[ICMP].code = icode
        ans = sr1(pkt, timeout=0.2)
        if ans:
            print(ans.show())
    #    for icode in range(0, 256):
    #        print(itype, icode)
        else:
            print("NOT ANSWER!!!")

    out = "{:>8} -> {:<8}"



    '''
    for pkt in pkts:
        #if not flags or all(i in pkt.sprintf(r"%TCP.flags%") for i in flags):
        print(pkt.show2())
        ans = sr1(pkt, timeout=0.2)
        if ans:
            #if not rflags or all(i in ans.sprintf(r"%TCP.flags%") for i in rflags):
            #print(out.format(pkt.sprintf(r"%TCP.flags%"), ans.sprintf(r"%TCP.flags%")))
            print(ans.show())
    '''

    return True

if __name__ == '__main__':
    cmd_icmp()

#from habu.lib.firewall_bsd import FirewallBSD
from habu.lib.firewall_iptables import FirewallIPTables
from habu.lib import delegator

class Firewall():

    def __init__(self):
        if delegator.run('which iptables', block=True).return_code == 0:
            self.__class__ = FirewallIPTables
            self.__init__()



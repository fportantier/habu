
from habu.lib import delegator
import ipaddress
import sys

class FirewallIPTables():

    def __init__(self):
        self.verbose = False

    def disable(self):
        commands = [
            'iptables -X',
            'iptables -F',
            'iptables -Z',
            'iptables -P INPUT ACCEPT',
            'iptables -P OUTPUT ACCEPT',
            'iptables -P FORWARD ACCEPT',
        ]

        for command in commands:
            if self.verbose:
                print(command)
            if delegator.run(command, block=True).return_code != 0:
                sys.stderr.write('Error. Do you have sufficient privileges?\n')
                return False

        return True

    def stealth(self):
        delegator.run('iptables -X')
        delegator.run('iptables -F')
        delegator.run('iptables -Z')
        delegator.run('iptables -P INPUT DROP')
        delegator.run('iptables -P OUTPUT ACCEPT')
        delegator.run('iptables -P FORWARD DROP')
        delegator.run('iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')

    def no_rst(self):
        commands = [
            'iptables -A OUTPUT -p tcp --tcp-flags rst rst -j DROP',
        ]

        for command in commands:
            if self.verbose:
                print(command)
            if delegator.run(command, block=True).return_code != 0:
                sys.stderr.write('Error. Do you have sufficient privileges?\n')
                return False

        return True

    def forward_enable():
        for f in ['/proc/sys/net/ipv4/ip_forward', '/proc/sys/net/ipv6/conf/all/forwarding']:
            with open(f, 'w') as target:
                target.write(1)

    def forward_disable():
        for f in ['/proc/sys/net/ipv4/ip_forward', '/proc/sys/net/ipv6/conf/all/forwarding']:
            with open(f, 'w') as target:
                target.write(0)

'''
    def disable(self):


  IPV4_PATH = "/proc/sys/net/ipv4"
  IP_FORWARD_PATH = IPV4_PATH + "/ip_forward"
  ICMP_BCAST_PATH = IPV4_PATH + "/icmp_echo_ignore_broadcasts"
  SEND_REDIRECTS_PATH = IPV4_PATH + "/conf/all/send_redirects"
  IPV6_PATH = "/proc/sys/net/ipv6"
  IPV6_FORWARD_PATH = IPV6_PATH + "/conf/all/forwarding"

  # If +enabled+ is true will enable packet forwarding, otherwise it will
  # disable it.
  def enable_ipv6_forwarding(enabled)
    File.open(IPV6_FORWARD_PATH,'w') { |f| f.puts "#{enabled ? 1 : 0}"}
  end

  # If +enabled+ is true will enable packet forwarding, otherwise it will
  # disable it.
  def enable_forwarding(enabled)
    File.open(IP_FORWARD_PATH,'w') { |f| f.puts "#{enabled ? 1 : 0}" }
  end

  # Return true if packet forwarding is currently enabled, otherwise false.
  def forwarding_enabled?
    File.open(IP_FORWARD_PATH) { |f| f.read.strip == '1' }
  end

  # Return true if packet forwarding for IPv6 is currently enabled, otherwise false.
  def ipv6_forwarding_enabled?
    File.open(IPV6_FORWARD_PATH) { |f| f.read.strip == '1' }
  end

  # If +enabled+ is true will enable packet icmp_echo_ignore_broadcasts, otherwise it will
  # disable it.
  def enable_icmp_bcast(enabled)
    File.open(ICMP_BCAST_PATH,'w') { |f| f.puts "#{enabled ? 1 : 0}" }
  end

  # If +enabled+ is true will enable send_redirects, otherwise it will
  # disable it.
  def enable_send_redirects(enabled)
    File.open(SEND_REDIRECTS_PATH,'w') { |f| f.puts "#{enabled ? 1 : 0}" }
  end

  # Apply the +r+ BetterCap::Firewalls::Redirection port redirection object.
  def add_port_redirection( r, use_ipv6 )
    table = 'iptables'
    cal_dst_address = r.dst_address
    if use_ipv6
      table = 'ip6tables'
      # Prevent sending out ICMPv6 Redirect packets.
      Shell.execute("#{table} -I OUTPUT -p icmpv6 --icmpv6-type redirect -j DROP")

      # Ipv6 uses a different ip + port representation
      cal_dst_address = "[#{r.dst_address}]"
    end
    # accept all
    Shell.execute("#{table} -P FORWARD ACCEPT")
    # add redirection
    Shell.execute("#{table} -t nat -A PREROUTING -i #{r.interface} -p #{r.protocol} #{r.src_address.nil? ? '' : "-d #{r.src_address}"} --dport #{r.src_port} -j DNAT --to #{cal_dst_address}:#{r.dst_port}")
  end

  # Remove the +r+ BetterCap::Firewalls::Redirection port redirection object.
  def del_port_redirection( r, use_ipv6 )
    table = 'iptables'
    cal_dst_address = r.dst_address
    if use_ipv6
      table = 'ip6tables'
      # Ipv6 uses a different ip + port representation
      cal_dst_address = "[#{r.dst_address}]"
    end
    # remove redirection
    Shell.execute("#{table} -t nat -D PREROUTING -i #{r.interface} -p #{r.protocol} #{r.src_address.nil? ? '' : "-d #{r.src_address}"} --dport #{r.src_port} -j DNAT --to #{cal_dst_address}:#{r.dst_port}")
  end
end
end
end
'''

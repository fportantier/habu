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
-   LAND Attack
-   SNMP Cracking
-   Subdomains Identification
-   SYN Flooding
-   TCP Flags Analysis
-   TCP ISN Analysis
-   TCP Port Scan
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

## habu.arpoison: ARP Poisoning

This command sends ARP 'is-at' packets to each victim, poisoning their
ARP tables for send the traffic to your system.

``` {.sourceCode .bash}
$ sudo habu.arpoison 192.168.1.5 192.168.1.6
Ether / ARP is at 00:c2:c6:30:2c:58 says 192.168.1.6
Ether / ARP is at 00:c2:c6:30:2c:58 says 192.168.1.5
Ether / ARP is at 00:c2:c6:30:2c:58 says 192.168.1.6
Ether / ARP is at 00:c2:c6:30:2c:58 says 192.168.1.5
...
```

**Note**: If you want a full working Man In The Middle attack, you need
to enable the packet forwarding on your operating system to act like a
router. You can do that using:

``` {.sourceCode .bash}
echo 1 > /proc/sys/net/ipv4/ip_forward
```

## habu.arpsniff: Discover devices on your LAN capturing ARP packets

This command listen for ARP packets and shows information each device.

Columns: Seconds from last packet | IP | MAC | Vendor

``` {.sourceCode .bash}
1   192.168.0.1     a4:08:f5:19:17:a4   Sagemcom Broadband SAS
7   192.168.0.2     64:bc:0c:33:e5:57   LG Electronics (Mobile Communications)
2   192.168.0.5     00:c2:c6:30:2c:58   Intel Corporate
6   192.168.0.7     54:f2:01:db:35:58   Samsung Electronics Co.,Ltd
```

## habu.contest: Check your connection capabilities

This command tries to connect to various services and check if you can
reach them using your internet connection.

``` {.sourceCode .bash}
$ habu.contest 
IP:    True
DNS:   True
FTP:   True
SSH:   True
HTTP:  True
HTTPS: True
```

## habu.ctfr: Subdomain mapping

This command downloads the certificate transparency logs for a domain
and check with DNS queries if each subdomain exists.

Uses multithreading to improve the performance of the DNS queries.

``` {.sourceCode .bash}
$ sudo habu.ctrf securetia.com
[
    "karma.securetia.com.",
    "www.securetia.com."
]
...
```

You can disable the DNS verification with the option '-n'.

**Note**: This command it's based on code from
<https://github.com/UnaPibaGeek/ctfr>

## habu.dhcp\_discover: Discover DHCP servers

This command send a DHCP request and shows what devices has replied.
Using the '-v' parameter (verbose) you can see all the options (like DNS
servers) included on the responses.

``` {.sourceCode .bash}
$ sudo habu.dhcp_discover 
Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.5:bootpc / BOOTP / DHCP
```

## habu.dhcp\_starvation: Fill the DHCP leases

This command send multiple DHCP requests from forged MAC addresses to
fill the DHCP server leases. When all the available network addresses
are assigned, the DHCP server don't send responses. So, some attacks,
like DHCP spoofing can be made.

``` {.sourceCode .bash}
$ sudo habu.dhcp_starvation 
Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.6:bootpc / BOOTP / DHCP
Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.7:bootpc / BOOTP / DHCP
Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.8:bootpc / BOOTP / DHCP
```

## habu.eicar: Prints the EICAR test string

This command prints the EICAR test string that can be used to test
antimalware engines. More info:
<http://www.eicar.org/86-0-Intended-use.html>

``` {.sourceCode .bash}
$ habu.eicar 
X5O!P%@AP[4\XZP54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
```

**Note:** The below string is incorrect because is not a good idea write
the complete in this text file. Some antivirus program can be detect it
like a virus. :)

## habu.hasher: Computes various hashes with the input data

This command computes various hashes for the input data, that can be a
file or a stream.

If the filename is '-', the data is taken from the standard input
(stdin) so, three different variants exists to call this command:

``` {.sourceCode .bash}
$ habu.hasher README.rst 
md5  : 375375d9cfb2aacab7c8d1a9afd3d9b7
sha1 : 21c67b9ef44bc24d47eef6adab648ba34662927e

$ cat README.rst | habu.hasher -
md5  : 375375d9cfb2aacab7c8d1a9afd3d9b7
sha1 : 21c67b9ef44bc24d47eef6adab648ba34662927e

$ habu.hasher - < README.rst 
md5  : 375375d9cfb2aacab7c8d1a9afd3d9b7
sha1 : 21c67b9ef44bc24d47eef6adab648ba34662927e
```

**Note:** The output above shows only MD5 and SHA1 to make it short, but
the real output includes more algorithms.

You can also specify which algorithm to use. In such case, the output is
only the value of the calculated hash:

``` {.sourceCode .bash}
$ habu.hasher -a md5 README.rst
375375d9cfb2aacab7c8d1a9afd3d9b7
```

## habu.ip: Prints your current public IP

This command prints your current public IP based on the response from
<https://api.ipify.org>.

``` {.sourceCode .bash}
$ habu.ip 
182.26.32.246
```

## habu.ip2asn: IP to ASN mapping
This command uses Team Cymru ip2asn service to get information about a public
IPv4/IPv6.

``` {.sourceCode .bash}
$ habu.ip2asn 8.8.8.8
{
    "asn": "15169",
    "net": "8.8.8.0/24",
    "cc": "US",
    "rir": "ARIN",
    "asname": "GOOGLE - Google LLC, US",
    "country": "United States"
}
```

## habu.isn: Prints the TCP sequence numbers for an IP

This command creates TCP connections and prints the TCP initial sequence
numbers for each connections.

``` {.sourceCode .bash}
$ sudo habu.isn www.portantier.com
1962287220
1800895007
589617930
3393793979
469428558
```

You can get a graphical representation (needs the matplotlib package)
using the '-g' option:

``` {.sourceCode .bash}
$ sudo habu.isn -g -c 10 www.portantier.com
```

![image](img/isn.png)

**Note:** The above command uses '-c' option to define that 10
connections must be created.

## habu.jshell: JavaScript Shell that uses WebSockets

This is one of the most complex commands in Habu. When you start it,
binds a port (default: 3333) and listen for HTTP connections. If
receives a connection, sends a JavaScript code that opens a WebSocket
(<https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API>) that
can be used to send commands to the connected browser.

You can write the commands directly in the shell, or use plugins, that
are simply external JavaScript files.

Using habu.jshell you can completely control a web browser.

**Note:** The complete documentation of the module will be separated
from the main documentation, because this module has a lot of options
and commands.

``` {.sourceCode .bash}
$ habu.jshell 
>>> Listening on 192.168.0.10:3333. Waiting for a victim connection.
>>> HTTP Request received from 192.168.0.15. Sending hookjs
>>> Connection from 192.168.0.15
$ _sessions
0 * 192.168.0.15:33432 Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0
$ _info
{
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "location": "http://192.168.0.10:3333/",
    "java-enabled": false,
    "platform": "Linux x86_64",
    "app-code-name": "Mozilla",
    "app-name": "Netscape",
    "app-version": "5.0 (X11)",
    "cookie-enabled": true,
    "language": "es-AR",
    "online": true
}
$ document.location
http://192.168.0.10:3333/
```

## habu.karma: Karma API client

Uses the Karma service (<https://karma.securetia.com>) to check an IP
against a lot of Threat Intelligence / Reputation lists.

``` {.sourceCode .bash}
habu.karma www.google.com
www.google.com -> 64.233.190.99
[
    "hphosts_fsa",
    "hphosts_psh",
    "hphosts_emd"
]
```

**Note:** You can use the hostname or the IP of the host to query.

## habu.land: Implements the LAND attack

This command implements the LAND attack, that sends packets forging the
source IP address to be the same that the destination IP. Also uses the
same source and destination port.

The attack is very old, and can be used to make a Denial of Service on
old systems, like Windows NT 4.0. More information here:
<https://en.wikipedia.org/wiki/LAND>

``` {.sourceCode .bash}
sudo habu.land 172.16.0.10
............
```

**Note:** Each dot (.) is a sent packet. You can specify how many
packets send with the '-c' option. The default is never stop. Also, you
can specify the destination port, with the '-p' option.

## habu.ping: ICMP echo requests

This command implements the classic 'ping' with ICMP echo requests.

``` {.sourceCode .bash}
$ sudo habu.ping 8.8.8.8
IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
IP / ICMP 8.8.8.8 > 192.168.0.5 echo-reply 0 / Padding
```

## habu.shodan: Shodan API client

This command is a simple shodan API client with prints the json result 
of a shodan query (or saves it on a file).

**Note:** Output cut for brevity.

``` {.sourceCode .bash}
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
            "data": "\nRecursion: enabled",
            "asn": "AS15169",
            "port": 53,
            "hostnames": [
                "google-public-dns-a.google.com"
            ],
            "location": {
                "longitude": -97.822,
                "country_code3": "USA",
                "latitude": 37.751000000000005,
                "country_code": "US",
                "country_name": "United States"
            }
        }
    ],
    "ports": [
        53
    ]
}
```

## habu.snmp\_crack: SNMP Community Cracker

This command launches snmp-get queries against an IP, and tells you when
finds a valid community string (is a simple SNMP cracker).

The dictionary used is the distributed with the onesixtyone tool
(<https://github.com/trailofbits/onesixtyone>)

``` {.sourceCode .bash}
$ sudo habu.snmp_crack 179.125.234.210 
Community found: private
Community found: public
```

**Note:** You can also receive messages like \<UNIVERSAL\> \<class
'scapy.asn1.asn1.ASN1\_Class\_metaclass'\>, I don't know how to supress
them for now.

## habu.synflood: SYN Flood Attack Implementation

This command launches a lot of TCP connections and keeps them opened.
Some very old systems can suffer a Denial of Service with this. More
info: <https://en.wikipedia.org/wiki/SYN_flood>

``` {.sourceCode .bash}
$ sudo habu.synflood 172.16.0.10
.................
```

Each dot is a packet sent.

You can use the options '-2' and '-3' to forge the layer 2/3 addresses.
If you use them, each connection will be sent from a random layer2 (MAC)
and/or layer3 (IP) address.

You can choose the number of connections to create with the option '-c'.
The default is never stop creating connections.

**Note:** If you send the packets from your real IP address and you want
to keep the connections half-open, you need to setup for firewall to
don't send the RST packets. With habu, you can do this with the
following command (only works with Linux+IPTables):

``` {.sourceCode .bash}
$ sudo habu.firewall --no-rst
```

You can check the results with "iptables -L -n", and you will see
something like this:

``` {.sourceCode .bash}
Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
DROP       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp flags:0x04/0x04
```

## habu.tcpflags: TCP Flag Fuzzer

This command send TCP packets with different flags and tell you what
responses receives.

It can be used to analyze how the different TCP/IP stack implementations
and configurations responds to packet with various flag combinations.

``` {.sourceCode .bash}
$ sudo habu.tcpflags www.portantier.com
S  -> SA
FS -> SA
FA -> R
SA -> R
```

By default, the command sends all possible flag combinations. You can
specify which flags must ever be present (reducing the quantity of
possible combinations), with the option '-f'.

Also, you can specify which flags you want to be present on the response
packets to show, with the option '-r'.

With the next command, you see all the possible combinations that have
the FIN (F) flag set and generates a response that contains the RST (R)
flag.

``` {.sourceCode .bash}
$ sudo habu.tcpflags -f F -r R www.portantier.com
FPA  -> R       
FSPA -> R       
FAU  -> R     
```

## habu.virustotal: VirusTotal API client

This command sends a file to VirusTotal <https://www.virustotal.com/> and 
prints the report in JSON format.

**Note:** Before send a file, habu will check if the file has been analyzed 
before (sending the sha256 of the file to VirusTotal), if a report exists, 
no submission will be made, and you will see the last report.

``` {.sourceCode .bash}
$ habu.virustotal meterpreter.exe

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
```


## habu.vhosts: Get vhosts of an IP address

This command uses Bing to query the websites hosted on the same IP
address.

``` {.sourceCode .bash}
$ habu.vhosts www.telefonica.com
www.telefonica.com -> 212.170.36.79
[
    'www.telefonica.es',
    'universitas.telefonica.com',
    'www.telefonica.com',
]
```

## habu.webid: Identify Web Technologies

This command uses Wappalyzer apps.json database to identify technologies
used on a web application.

More info about Wappalyzer: <https://github.com/AliasIO/Wappalyzer/>

**Note:** This tool only sends one request. So, it's stealth and not
suspicious.

``` {.sourceCode .bash}
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
```

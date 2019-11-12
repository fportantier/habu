.. Habu documentation master file, created by
   sphinx-quickstart on Sat Apr 27 22:04:26 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Habu Hacking Toolkit
====================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://img.shields.io/pypi/l/habu.svg
    :target: https://pypi.org/project/habu/

.. image:: https://img.shields.io/pypi/pyversions/habu.svg
    :target: https://pypi.org/project/habu/


The reason to develop Habu is (mainly) teach and learn about Python and Hacking.

Most of the functions implemented helps with some tasks for Ethical Hacking and
Penetration Testing.

The implementations are intended to be understandable for who wants to read the
source code and learn from that.

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

The User Guide
--------------

This part of the documentation, begins with some background information about Habu,
and how to install it.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install


Commands Usage Guide
--------------------

This part of the documentation, tells you how to use each command in the toolkit.

.. toctree::
   :maxdepth: 2

   commands/arp.ping


Library Usage Guide
-------------------

This part of the documentation, tells you how to use the habu library to integrate
the functionality into your own software.

.. toctree::
   :maxdepth: 2

   library/*
 

 

The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for 
you.

.. toctree::
   :maxdepth: 3

   contributing

There are no more guides. You are now guideless.
Good luck.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='habu',
    version='0.0.82',
    description='Python Network Hacking Toolkit',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Fabian Martinez Portantier',
    author_email='fabian@portantier.com',
    url='https://github.com/portantier/habu',
    license='Copyright Fabian Martinez Portantier',
    install_requires=[
        'beautifulsoup4',
        'cryptography',
        'click',
        'dnspython',
        'lxml',
        'prompt_toolkit==1.0.15',
        'pycrypto',
        'pygments',
        'regex',
        'requests',
        'requests-cache',
        #'scapy-python3',
        'scapy',
        'websockets',
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    entry_points='''
        [console_scripts]
        habu.arp.ping=habu.cli.cmd_arp_ping:cmd_arp_ping
        habu.arp.poison=habu.cli.cmd_arp_poison:cmd_arp_poison
        habu.arp.sniff=habu.cli.cmd_arp_sniff:cmd_arp_sniff
        habu.asydns=habu.cli.cmd_asydns:cmd_asydns
        habu.b64=habu.cli.cmd_b64:cmd_b64
        habu.certclone=habu.cli.cmd_certclone:cmd_certclone
        habu.config=habu.cli.cmd_config:cmd_config
        habu.config.set=habu.cli.cmd_config_set:cmd_config_set
        habu.config.del=habu.cli.cmd_config_del:cmd_config_del
        habu.contest=habu.cli.cmd_contest:cmd_contest
        habu.crack.luhn=habu.cli.cmd_crack_luhn:cmd_crack_luhn
        habu.crack.snmp=habu.cli.cmd_crack_snamp:cmd_crack_snmp
        habu.ctfr=habu.cli.cmd_ctfr:cmd_ctfr
        habu.cve.2018.9995=habu.cli.cmd_cve_2018_9995:cmd_cve_2018_9995
        habu.dhcp.discover=habu.cli.cmd_dhcp_discover:cmd_dhcp_discover
        habu.dhcp.starvation=habu.cli.cmd_dhcp_starvation:cmd_dhcp_starvation
        habu.eicar=habu.cli.cmd_eicar:cmd_eicar
        habu.extract.ipv4=habu.cli.cmd_extract_ipv4:cmd_extract_ipv4
        habu.extract.email=habu.cli.cmd_extract_email:cmd_extract_email
        habu.fernet=habu.cli.cmd_fernet:cmd_fernet
        habu.fernet.genkey=habu.cli.cmd_fernet_genkey:cmd_fernet_genkey
        habu.forkbomb=habu.cli.cmd_forkbomb:cmd_forkbomb
        habu.hasher=habu.cli.cmd_hasher:cmd_hasher
        habu.ip=habu.cli.cmd_ip:cmd_ip
        habu.ip2asn=habu.cli.cmd_ip2asn:cmd_ip2asn
        habu.isn=habu.cli.cmd_isn:cmd_isn
        habu.jshell=habu.cli.cmd_jshell:cmd_jshell
        habu.karma=habu.cli.cmd_karma:cmd_karma
        habu.land=habu.cli.cmd_land:cmd_land
        habu.nc=habu.cli.cmd_nc:cmd_nc
        habu.ping=habu.cli.cmd_ping:cmd_ping
        habu.protoscan=habu.cli.cmd_protoscan:cmd_protoscan
        habu.server.ftp=habu.cli.cmd_server_ftp:cmd_server_ftp
        habu.shodan=habu.cli.cmd_shodan:cmd_shodan
        habu.synflood=habu.cli.cmd_synflood:cmd_synflood
        habu.tcpflags=habu.cli.cmd_tcpflags:cmd_tcpflags
        habu.tcpscan=habu.cli.cmd_tcpscan:cmd_tcpscan
        habu.traceroute=habu.cli.cmd_traceroute:cmd_traceroute
        habu.usercheck=habu.cli.cmd_usercheck:cmd_usercheck
        habu.vhosts=habu.cli.cmd_vhosts:cmd_vhosts
        habu.virustotal=habu.cli.cmd_virustotal:cmd_virustotal
        habu.webid=habu.cli.cmd_webid:cmd_webid
        habu.xor=habu.cli.cmd_xor:cmd_xor
    ''',
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['habu', 'habu.lib', 'habu.lib.completeme', 'habu.cli'],
    include_package_data=True,
    keywords=['security'],
    zip_safe=False,
    test_suite='py.test',
)

from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='habu',
    version='0.0.50',
    description='Python Network Hacking Toolkit',
    long_description=readme,
    author='Fabian Martinez Portantier',
    author_email='fabian@portantier.com',
    url='https://github.com/portantier/habu',
    license='Copyright Fabian Martinez Portantier',
    install_requires=[
        #'bs4',
        'beautifulsoup4',
        'click',
        'regex',
        'requests',
        'requests-cache',
        'scapy-python3',
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    entry_points='''
        [console_scripts]
        habu.arping=habu.cli.cmd_arping:cmd_arping
        habu.arpoison=habu.cli.cmd_arpoison:cmd_arpoison
        habu.arpsniff=habu.cli.cmd_arpsniff:cmd_arpsniff
        habu.b64=habu.cli.cmd_b64:cmd_b64
        habu.contest=habu.cli.cmd_contest:cmd_contest
        habu.ctfr=habu.cli.cmd_ctfr:cmd_ctfr
        habu.dhcp_discover=habu.cli.cmd_dhcp_discover:cmd_dhcp_discover
        habu.dhcp_starvation=habu.cli.cmd_dhcp_starvation:cmd_dhcp_starvation
        habu.eicar=habu.cli.cmd_eicar:cmd_eicar
        habu.firewall=habu.cli.cmd_firewall:cmd_firewall
        habu.forkbomb=habu.cli.cmd_forkbomb:cmd_forkbomb
        habu.hasher=habu.cli.cmd_hasher:cmd_hasher
        habu.help=habu.cli.cmd_help:cmd_help
        habu.hex2ascii=habu.cli.cmd_hex2ascii:cmd_hex2ascii
        habu.ip=habu.cli.cmd_ip:cmd_ip
        habu.ip2asn=habu.cli.cmd_ip2asn:cmd_ip2asn
        habu.isn=habu.cli.cmd_isn:cmd_isn
        habu.karma=habu.cli.cmd_karma:cmd_karma
        habu.land=habu.cli.cmd_land:cmd_land
        habu.ping=habu.cli.cmd_ping:cmd_ping
        habu.snmp_crack=habu.cli.cmd_snmp_crack:cmd_snmp_crack
        habu.tcpflags=habu.cli.cmd_tcpflags:cmd_tcpflags
        habu.tcpscan=habu.cli.cmd_tcpscan:cmd_tcpscan
        habu.traceroute=habu.cli.cmd_traceroute:cmd_traceroute
        habu.synflood=habu.cli.cmd_synflood:cmd_synflood
        habu.webid=habu.cli.cmd_webid:cmd_webid
        habu.vhosts=habu.cli.cmd_vhosts:cmd_vhosts
        habu.xor=habu.cli.cmd_xor:cmd_xor
    ''',
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['habu', 'habu.lib', 'habu.cli'],
    include_package_data=True,
    keywords=['security'],
    zip_safe=False,
    test_suite='py.test',
)

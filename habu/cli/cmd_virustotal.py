import hashlib
import json
import logging
import os
import sys
from pathlib import Path
from time import sleep

import click
import requests

from habu.lib.loadcfg import loadcfg


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_shodan(input, output, verbose):

    habucfg = loadcfg()

    if 'VIRUSTOTAL_APIKEY' not in habucfg:
        logging.error('You must provide a virustotal apikey. Use the ~/.habu.json file (variable VIRUSTOTAL_APIKEY), or export the variable HABU_VIRUSTOTAL_APIKEY')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    filename = Path(input.name).name

    data = input.read()

    sha256 = hashlib.sha256(data).hexdigest()

    logging.info('Verifying if hash already submitted: {}'.format(sha256))

    params = {'apikey': habucfg['VIRUSTOTAL_APIKEY'], 'resource': sha256}
    response = requests.post('https://www.virustotal.com/vtapi/v2/file/rescan', params=params)
    json_response = response.json()

    if json_response['response_code'] == 0:
        files = {'file': (filename, data)}
        params = {'apikey': habucfg['VIRUSTOTAL_APIKEY']}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
        json_response = response.json()

        resource = json_response['resource']

    logging.info('Waiting/retrieving the report...')

    while True:
        params = {'apikey': habucfg['VIRUSTOTAL_APIKEY'], 'resource': sha256}
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
        json_response = response.json()

        if json_response['response_code'] == 1:
            break

        sleep(5)

    output.write(json.dumps(json_response, indent=4, sort_keys=True))
    output.write('\n')

if __name__ == '__main__':
    cmd_shodan()

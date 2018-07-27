#!/usr/bin/env python3

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
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_virustotal(input, verbose):
    """Send a file to VirusTotal https://www.virustotal.com/ and print the report in JSON format.

    Note: Before send a file, habu will check if the file has been analyzed before (sending the
    sha256 of the file to VirusTotal), if a report exists, no submission will be made, and you will
    see the last report.

    \b
    $ habu.virustotal meterpreter.exe
    Verifying if hash already submitted: f4826b219aed3ffdaa23db26cfae611979bf215984fc71a1c12f6397900cb70d
    Sending file for analysis
    Waiting/retrieving the report...
    {
        "md5": "0ddb015b5328eb4d0cc2b87c39c49686",
        "permalink": "https://www.virustotal.com/file/c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23/analysis/1526850717/",
        "positives": 49,
        "resource": "c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23",
        "response_code": 1,
        "scan_date": "2018-05-20 21:11:57",
        "scan_id": "c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23-1526850717",
        "scans": {
            "ALYac": {
                "detected": true,
                "result": "Trojan.CryptZ.Gen",
                "update": "20180520",
                "version": "1.1.1.5"
            },
            ... The other scanners ...
        },
        "sha1": "5fa33cab1729480dd023b08f7b91a945c16d0a9e",
        "sha256": "c9a2252b491641e15753a4d0c4bb30b1f9bd26ecff2c74f20a3c7890f3a1ea23",
        "total": 67,
        "verbose_msg": "Scan finished, information embedded"
    }
    """

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

    if response.status_code != 200 or response.json()['response_code'] == 0:
        logging.info('Sending file for analysis')
        files = {'file': (filename, data)}
        params = {'apikey': habucfg['VIRUSTOTAL_APIKEY']}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
        json_response = response.json()

        resource = json_response['resource']

    logging.info('Waiting/retrieving the report...')

    while True:
        params = {'apikey': habucfg['VIRUSTOTAL_APIKEY'], 'resource': sha256}
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)

        if response.status_code == 200:
            json_response = response.json()
            if json_response['response_code'] == 1:
                break

        sleep(5)

    print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == '__main__':
    cmd_virustotal()

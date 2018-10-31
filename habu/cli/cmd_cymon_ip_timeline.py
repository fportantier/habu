#!/usr/bin/env python3

import json
import logging
import os
import os.path
import pwd
import sys

import click
import requests
import requests_cache

from habu.lib.loadcfg import loadcfg

def pretty_print(data):

    output = ''

    for timeline in reversed(data['timeline']):
        for event in timeline['events']:
            output += '{} {}\n'.format(event['created'], event['title'])

    return output


@click.command()
@click.argument('ip')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
@click.option('-p', 'pretty', is_flag=True, default=False, help='Pretty output')
def cmd_cymon_ip_timeline(ip, no_cache, verbose, output, pretty):
    """Simple cymon API client.

    Prints the JSON result of a cymon IP timeline query.

    Example:

    \b
    $ habu.cymon.ip.timeline 8.8.8.8
    {
        "timeline": [
            {
                "time_label": "Aug. 18, 2018",
                "events": [
                    {
                        "description": "Posted: 2018-08-18 23:37:39 CEST IDS Alerts: 0 URLQuery Alerts: 1 ...",
                        "created": "2018-08-18T21:39:07Z",
                        "title": "Malicious activity reported by urlquery.net",
                        "details_url": "http://urlquery.net/report/b1393866-9b1f-4a8e-b02b-9636989050f3",
                        "tag": "malicious activity"
                    }
                ]
            },
            ...
    """

    habucfg = loadcfg()

    if 'CYMON_APIKEY' not in habucfg:
        print('You must provide a cymon apikey. Use the ~/.habu.json file (variable CYMON_APIKEY), or export the variable HABU_CYMON_APIKEY')
        print('Get your API key from https://www.cymon.io/')
        sys.exit(1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')

    url = 'https://www.cymon.io:443/api/nexus/v1/ip/{}/timeline/'.format(ip)
    headers = { 'Authorization': 'Token {}'.format(habucfg['CYMON_APIKEY']) }

    r = requests.get(url, headers=headers)

    if r.status_code not in [200, 404]:
        print('ERROR', r)
        return False

    if r.status_code == 404:
        print("Not Found")
        return False

    data = r.json()

    if pretty:
        output.write(pretty_print(data))
    else:
        output.write(json.dumps(data, indent=4))
        output.write('\n')

if __name__ == '__main__':
    cmd_cymon_ip_timeline()

# based on code from https://github.com/UnaPibaGeek/ctfr

import json
import logging

import click
import requests
import requests_cache

from habu.lib.dns import query_bulk

requests_cache.install_cache('/tmp/habu_requests_cache')

@click.command()
@click.argument('domain')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-n', 'no_validate', is_flag=True, default=False, help='Disable DNS subdomain validation')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_ctfr(domain, no_cache, no_validate, verbose):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        requests_cache.install_cache('/tmp/habu_requests_cache')

    subdomains = set()

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=domain))

    if req.status_code != 200:
        print("[X] Information not available!")
        exit(1)

    json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

    for data in json_data:
        name = data['name_value'].lower()
        if '*' not in name:
            subdomains.add(name)

    subdomains = list(subdomains)

    if no_validate:
        print(json.dumps(sorted(subdomains), indent=4))
        return True

    answers = query_bulk(subdomains)

    validated = []

    for answer in answers:
        if answer:
            validated.append(str(answer.qname))

    print(json.dumps(sorted(validated), indent=4))
    return True


if __name__ == '__main__':
    cmd_ctfr()

import json
import logging

import click
import regex as re


def extract_ipv4(data):

    regexp = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', flags=re.MULTILINE)

    match = regexp.finditer(data)

    result = []

    for m in match:
        result.append(m.group(0))

    return result

def extract_email(data):

    regexp = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

    match = regexp.finditer(data)

    result = []

    for m in match:
        result.append(m.group(0))

    return result


@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-j', 'jsonout', is_flag=True, default=False, help='JSON output')
@click.option('-w', 'what', required=True, type=click.Choice(['email', 'ipv4']), help='What do you want to extract')
def cmd_extract(infile, verbose, jsonout, what):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = []

    functions = {
        'ipv4' : extract_ipv4,
        'email' : extract_email,
    }

    result = functions[what](data)

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_extract()

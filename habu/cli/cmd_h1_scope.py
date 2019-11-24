#!/usr/bin/env python3

import click
import json
import logging

@click.command()
@click.option('-j', 'json_output', is_flag=True, default=False, help='Output in JSON format')
@click.argument('infile', type=click.File('r'), default='-')
def cmd_h1_scope(infile, json_output):
    """Parse HackerOne scope specification in BurpSuite JSON format

    Example:

    \b
    $ habu.h1.scope starbucks.json
    app.starbucks.com
    card.starbucks.com.sg
    cart.starbucks.co.jp
    ec.starbucks.com.cn
    gift.starbucks.co.jp
    login.starbucks.co.jp
    preview.starbucks.com
    www.istarbucks.co.kr
    www.starbucks.ca
    www.starbucks.co.jp
    www.starbucks.co.uk
    www.starbucks.com
    www.starbucks.com.br
    www.starbucks.com.cn
    www.starbucks.com.sg
    www.starbucks.de
    www.starbucks.fr
    www.starbucksreserve.com
    www.teavana.com
    """

    try:
        data = json.loads(infile.read())
    except Exception:
        logging.error('Can\'t parse json file')
        return False

    domains = set()

    for item in data['target']['scope']['include']:
        domains.add(item['host'].strip('^').strip('$').replace('\\', ''))

    if json_output:
        print(json.dumps(sorted(domains), indent=4))
    else:
        print('\n'.join(sorted(domains)))


if __name__ == '__main__':
    cmd_h1_scope()

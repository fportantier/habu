#!/usr/bin/env python3

import json

import click

from habu.lib.http_tech import http_tech


@click.command()
@click.argument('url')
@click.option('--cache/--no-cache', 'cache', default=True)
@click.option('--format', 'output_format', type=click.Choice(['txt', 'csv','json']), default='txt', help='Output format')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_http_tech(url, cache, output_format, verbose):
    """Uses Wappalyzer apps.json database to identify technologies used on a web application.

    Reference: https://github.com/AliasIO/Wappalyzer

    Note: This tool only sends one request. So, it's stealth and not suspicious.

    \b
    $ habu.web.tech https://woocomerce.com
    Google Tag Manager       unknown
    MySQL                    unknown
    Nginx                    unknown
    PHP                      unknown
    Prototype                unknown
    RequireJS                unknown
    WooCommerce              3.8.0
    WordPress                5.2.4
    Yoast SEO                10.0.1
    """

    response = http_tech(url, cache=cache, verbose=verbose)

    if output_format == 'json':
        print(json.dumps(response, indent=4))
        return True

    for tech, data in response.items():
        if 'version' not in data:
            data['version'] = 'unknown'

        if output_format == 'csv':
            print('"{}","{}","{}"'.format(url, tech, data['version']))
        else:
            print('{:<25}{}'.format(tech, data['version']))


if __name__ == '__main__':
    cmd_http_tech()

#!/usr/bin/env python3

import json

import click

from habu.lib.web_tech import web_tech


@click.command()
@click.argument('url')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_web_tech(url, no_cache, verbose):
    """Use Wappalyzer apps.json database to identify technologies used on a web application.

    Reference: https://github.com/AliasIO/Wappalyzer

    Note: This tool only sends one request. So, it's stealth and not suspicious.

    \b
    $ habu.web.tech https://woocomerce.com
    {
        "Nginx": {
            "categories": [
                "Web Servers"
            ]
        },
        "PHP": {
            "categories": [
                "Programming Languages"
            ]
        },
        "WooCommerce": {
            "categories": [
                "Ecommerce"
            ],
            "version": "6.3.1"
        },
        "WordPress": {
            "categories": [
                "CMS",
                "Blogs"
            ]
        },
    }
    """

    response = web_tech(url, no_cache, verbose)
    print(json.dumps(response, indent=4))


if __name__ == '__main__':
    cmd_web_tech()

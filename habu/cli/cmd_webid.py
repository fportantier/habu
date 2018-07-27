#!/usr/bin/env python3

import json
import os
import os.path
from pathlib import Path

import click

from habu.lib.webid import webid

@click.command()
@click.argument('url')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_webid(url, no_cache, verbose):
    """Use Wappalyzer apps.json database to identify technologies used on a web application.

    Reference: https://github.com/AliasIO/Wappalyzer

    Note: This tool only sends one request. So, it's stealth and not suspicious.

    \b
    $ habu.webid https://woocomerce.com
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

    response = webid(url, no_cache, verbose)
    print(json.dumps(response, indent=4))

if __name__ == '__main__':
    cmd_webid()

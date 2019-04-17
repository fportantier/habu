#!/usr/bin/env python3

import html
import sys
from pathlib import Path

import click
from json2table import convert

from habu.lib.http import get_headers, get_options
from habu.lib.web_screenshot import web_screenshot


@click.command()
@click.option('-v', 'verbose', is_flag=True, default=False,
              help='Verbose output.')
@click.argument('urls', type=click.File('rb'), default='-')
@click.option('-b', 'browser', default='firefox',
              type=click.Choice(['firefox', 'chromium-browser']),
              help='Browser to use for screenshot.')
def cmd_web_report(urls, browser, verbose):
    """Use a browser to take a screenshot of the websites.

    Makes a report that includes the HTTP headers.

    The expected format for the input file is one URL per line.

    Create a directory called 'report' with the content inside.

    \b
    $ echo https://www.portantier.com | habu.web.report

    $ habu.web.report urls.txt
    """
    table_attributes = {
        "style": "width:100%,text-align:left",
        "class": "table table-striped",
    }
    build_direction = "LEFT_TO_RIGHT"
    urls = urls.read().decode().strip().split('\n')
    report_dir = Path('report')

    try:
        report_dir.mkdir()
    except Exception:
        pass

    report_file = report_dir / 'index.html'

    with report_file.open('w') as outfile:
        outfile.write('<!doctype html>\n')
        outfile.write('<html lang=en-us>\n')
        outfile.write('<meta charset=utf-8>\n')
        outfile.write('<title>habu.web.report</title>\n')
        outfile.write('<body>\n')

        for index, url in enumerate(sorted(urls)):
            print(index, url, file=sys.stderr)

            outfile.write('<h1>' + html.escape(url) + '</h1>\n')
            try:
                outfile.write('<h2>Headers</h2>\n')
                headers = get_headers(url)
                outfile.write(convert(
                    headers, build_direction=build_direction,
                    table_attributes=table_attributes))
                outfile.write('\n')
                outfile.write('<h2>Allowed options</h2>\n')
                options = get_options(url)
                outfile.write(convert(options))
                outfile.write('\n')
            except AttributeError:
                outfile.write('<pre>ERROR: Unable to retrieve details</pre>\n')

            outfile.write('<h2>Screenshot</h2>\n')
            web_screenshot(url, report_dir / '{}.png'.format(index), browser)

            if (report_dir / '{}.png'.format(index)).is_file():
                outfile.write(
                    '<p><img src={}.png style="max-width:80%"/></p>\n'.format(index))
            else:
                outfile.write(
                    '<pre>ERROR: Unable to create screenshot</pre>\n')

        outfile.write('</body>\n')
        outfile.write('</html>\n')


if __name__ == '__main__':
    cmd_web_report()

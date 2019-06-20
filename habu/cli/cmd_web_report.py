#!/usr/bin/env python3

import html
import sys
import urllib.request
import requests
from pathlib import Path
import urllib3

import click

from habu.lib.web_screenshot import web_screenshot

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@click.command()
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-s', 'screenshot', is_flag=True, default=False, help='Take a screenshot for each website')
@click.option('-b', 'browser', default=None, type=click.Choice(['firefox', 'chromium-browser']), help='Browser to use for screenshot.')
@click.argument('input_file', type=click.File('rb'), default='-')
def cmd_web_report(input_file, verbose, browser, screenshot):
    """Makes a report that includes HTTP headers of websites.

    Optionally, uses Firefox or Chromium to take a screenshot of the websites.

    The expected format is one url per line.

    Creates a directory called 'report' with the content inside.

    \b
    $ echo https://www.portantier.com | habu.web.report
    """

    urls = input_file.read().decode().strip().split('\n')

    urls = [ url.strip() for url in urls if url.strip() ]

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
        outfile.write('<table border=1 style="max-width: 100%">\n')

        for i,url in enumerate(sorted(urls)):

            error = False

            print(i, url, file=sys.stderr)

            outfile.write('<tr>\n')
            outfile.write('<td style="vertical-align:top;max-width:30%">\n')
            outfile.write('<p><strong>' + html.escape(url) + '</strong></p>\n')

            try:
                response = requests.head(url, verify=False, timeout=3)

                headers = 'Status Code: {}\n'.format(response.status_code)
                for name,value in response.headers.items():
                    headers += '{}: {}\n'.format(name, value)

                outfile.write('<pre style="white-space: pre-wrap;">' + html.escape(headers) + '</pre>\n')
            except Exception as e:
                outfile.write('<pre>ERROR: ' + html.escape(str(e)) + '</pre>\n')
                error = True

            outfile.write('</td><td>')

            if screenshot and not error:
                web_screenshot(url, report_dir / '{}.png'.format(i), browser=browser)
                outfile.write('<img src={}.png style="max-width: 100%" />\n'.format(i))

            outfile.write('</td>\n')
            outfile.write('</tr>\n')

        outfile.write('</table>\n')
        outfile.write('</body>\n')
        outfile.write('</html>\n')


if __name__ == '__main__':
    cmd_web_report()

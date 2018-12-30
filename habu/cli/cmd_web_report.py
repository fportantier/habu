#!/usr/bin/env python3

import html
import sys
import urllib.request
from pathlib import Path

import click

from habu.lib.web_screenshot import web_screenshot


@click.command()
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.argument('f', type=click.File('rb'), default='-')
def cmd_web_report(f, verbose):
    """Uses Firefox to take a screenshot of the websites. (you need firefox installed, obviously)

    Makes a report that includes the HTTP headers.

    The expected format is one url per line.

    Creates a directory called 'report' with the content inside.

    \b
    $ echo https://www.portantier.com | habu.web.report
    """

    urls = f.read().decode().strip().split('\n')

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
                req = urllib.request.Request(url, method='HEAD')
                resp = urllib.request.urlopen(req)
                outfile.write('<pre style="white-space: pre-wrap;">' + html.escape(str(resp.headers)) + '</pre>\n')
            except Exception as e:
                outfile.write('<pre>ERROR: ' + html.escape(str(e)) + '</pre>\n')
                error = True

            outfile.write('</td><td>')

            if not error:
                web_screenshot(url, report_dir / '{}.png'.format(i))
                outfile.write('<img src={}.png style="max-width: 100%" />\n'.format(i))

            outfile.write('</td>\n')
            outfile.write('</tr>\n')

        outfile.write('</table>\n')
        outfile.write('</body>\n')
        outfile.write('</html>\n')


if __name__ == '__main__':
    cmd_web_report()

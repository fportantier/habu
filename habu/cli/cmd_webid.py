import json
import logging
import sys
from pprint import pprint
import os.path

import click
import regex as re
import requests
import requests_cache
from bs4 import BeautifulSoup
from pathlib import Path

DATADIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))

@click.command()
@click.argument('url')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-o', 'output', type=click.File('w'), default='-', help='Output file (default: stdout)')
def cmd_webid(url, no_cache, verbose, output):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        requests_cache.install_cache('/tmp/habu_requests_cache')

    try:
        r = requests.get(url)
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    with (DATADIR / 'apps.json').open() as f:
        data = json.load(f)

    apps = data['apps']
    categories = data['categories']

    # convertir los strings a listas, para que siempre los valores sean listas
    for app in apps:
        for field in ['url', 'html', 'env', 'script', 'implies', 'excludes']:

            if field in apps[app]:
                if not isinstance(apps[app][field], list):
                    apps[app][field] = [apps[app][field]]

    content = r.text
    soup = BeautifulSoup(content, "lxml")
    tech = {}

    with open('/tmp/habu.webid.html', 'w') as out:
        out.write(content)

    # pprint(dict(r.headers))

    for app in apps:

        version_group = False

        for header in apps[app].get('headers', []):
            if header in r.headers:

                header_regex = apps[app]['headers'][header].split('\;')[0]

                if '\;version:\\' in apps[app]['headers'][header]:
                    version_group = apps[app]['headers'][header].split('\;version:\\')[1]

                match = re.search(header_regex, r.headers[header], flags=re.IGNORECASE)
                if match or not header_regex:
                    logging.info("{app} detected by {header} HTTP header = {header_content}".format(app=app, header=header, header_content=r.headers[header]))
                    if app not in tech:
                        tech[app] = apps[app]

                    if version_group and version_group.isdigit():
                        version = match.group(int(version_group))
                        if version:
                            tech[app]['version'] = version

        for key in ['script', 'html']:

            version_group = False

            for item in apps[app].get(key, []):
                item_regex = item.split('\;')[0]

                if '\;version:\\' in item:
                    version_group = item.split('\;version:\\')[1]

                match = re.search(item_regex, r.text, flags=re.IGNORECASE & re.MULTILINE)
                if match:
                    logging.info("{app} detected by HTML body with regex {regex}".format(app=app, regex=item_regex))
                    if app not in tech:
                        tech[app] = apps[app]

                    if version_group and version_group.isdigit():
                        version = match.group(int(version_group))
                        if version:
                            tech[app]['version'] = version

        for url_regex in apps[app].get('url', []):
            match = re.search(url_regex, url, flags=re.IGNORECASE & re.MULTILINE)
            if match:
                logging.info("{app} detected by URL with regex {regex}".format(app=app, regex=url_regex))
                if app not in tech:
                    tech[app] = apps[app]

        for meta in apps[app].get('meta', []):

            version_group = False

            for tag in soup.find_all("meta", attrs={'name': meta}):
                meta_regex = apps[app]['meta'][meta]

                if '\;version:\\' in meta_regex:
                    version_group = meta_regex.split('\;version:\\')[1]

                meta_regex = meta_regex.split('\;')[0]
                match = re.search(meta_regex, tag['content'], flags=re.IGNORECASE)

                if match:
                    logging.info("{app} detected by meta {meta} tag with regex {regex}".format(app=app, meta=meta, regex=meta_regex))

                    if app not in tech:
                        tech[app] = apps[app]

                    if version_group and version_group.isdigit():
                        version = match.group(int(version_group))
                        if version:
                            tech[app]['version'] = version

    for t in list(tech.keys()):
        for imply in tech[t].get('implies', []):
            logging.info("{imply} detected because implied by {t}".format(imply=imply, t=t))
            tech[imply] = apps[imply]

    for t in list(tech.keys()):
        tech[t]['category'] = categories[tech[t]['cats'][0]]['name']

    for t in list(tech.keys()):
        for exclude in tech[t].get('excludes', []):
            logging.info("removing {exlude} because its excluded by {t}".format(exlude=exclude, t=t))
            del(tech[t])

    response = []
    for t in sorted(tech):
        if 'version' in tech[t]:
            response.append('{app} {version}'.format(app=t, version=version))
        else:
            response.append('{app}'.format(app=t))

    output.write(json.dumps(response, indent=4))

if __name__ == '__main__':
    cmd_webid()

import json
import logging
import os
import os.path
import pwd
from pathlib import Path

import regex as re
import requests
import requests_cache
from bs4 import BeautifulSoup

DATADIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))

def webid(url, no_cache=False, verbose=False):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')

    try:
        r = requests.get(url)
    except Exception as e:
        logging.error(e)
        return False

    with (DATADIR / 'apps-habu.json').open() as f:
        data = json.load(f)

    apps = data['apps']
    categories = data['categories']

    content = r.text
    soup = BeautifulSoup(content, "lxml")
    tech = {}

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
                        try:
                            version = match.group(int(version_group))
                            if version:
                                tech[app]['version'] = version
                        except IndexError:
                            pass

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

                        try:
                            version = match.group(int(version_group))
                            if version:
                                tech[app]['version'] = version
                        except IndexError:
                            pass

        for url_regex in apps[app].get('url', []):
            match = re.search(url_regex, url, flags=re.IGNORECASE & re.MULTILINE)
            if match:
                logging.info("{app} detected by URL with regex {regex}".format(app=app, regex=url_regex))
                if app not in tech:
                    tech[app] = apps[app]

        for cookie_name in apps[app].get('cookies', []):

            for cookie in r.cookies:
                if cookie_name == cookie.name:
                    logging.info("{app} detected by cookie {cookie}".format(app=app, cookie=cookie.name))

                    if app not in tech:
                        tech[app] = apps[app]

        for meta in apps[app].get('meta', []):

            version_group = False

            for tag in soup.find_all("meta", attrs={'name': meta}):
                meta_regex = apps[app]['meta'][meta]

                if '\;version:\\' in meta_regex:
                    version_group = meta_regex.split('\;version:\\')[1]

                meta_regex = meta_regex.split('\;')[0]

                try:
                    match = re.search(meta_regex, tag['content'], flags=re.IGNORECASE)
                except KeyError:
                    continue

                if match:
                    logging.info("{app} detected by meta {meta} tag with regex {regex}".format(app=app, meta=meta, regex=meta_regex))

                    if app not in tech:
                        tech[app] = apps[app]

                    if version_group and version_group.isdigit():

                        try:
                            version = match.group(int(version_group))
                            if version:
                                tech[app]['version'] = version
                        except IndexError:
                            pass

    for t in list(tech.keys()):
        for imply in tech[t].get('implies', []):
            imply = imply.split('\\;')[0]
            logging.info("{imply} detected because implied by {t}".format(imply=imply, t=t))
            tech[imply] = apps[imply]

    for t in list(tech.keys()):
        for exclude in tech[t].get('excludes', []):
            logging.info("removing {exlude} because its excluded by {t}".format(exlude=exclude, t=t))
            del(tech[t])

    response = {}

    for t in sorted(tech):
        response[t] = {'categories':[]}
        if 'version' in tech[t]:
            response[t]['version'] = version
        for category in tech[t]['cats']:
            response[t]['categories'].append(categories[str(category)]['name'])

    return response

if __name__ == '__main__':
    print(webid('https://www.woocommerce.com'))


import json
import logging
import re
import sys
from pprint import pprint

import click
import regex as re
import requests
import requests_cache
from bs4 import BeautifulSoup

requests_cache.install_cache('/tmp/habu_requests_cache')

@click.command()
@click.argument('url')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_weburls(url, no_cache, verbose):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    #if not no_cache:
    #    requests_cache.install_cache('/tmp/habu_requests_cache')


    search(url)

    sys.exit(0)

    with open('../data/apps.json') as f:
        data = json.load(f)

    apps = data['apps']
    categories = data['categories']

    # convertir los strings a listas, para que siempre los valores sean listas
    for app in apps:
        for field in ['url', 'html', 'env', 'script', 'implies', 'excludes']:

            if field in apps[app]:
                if type(apps[app][field]) != type([]):
                    apps[app][field] = [apps[app][field]]

    for app in apps:

        for url_regex in apps[app].get('url', []):
            match = re.search(url_regex, url, flags=re.IGNORECASE & re.MULTILINE)
            if match:
                print("{app} detected by URL with regex {regex}".format(app=app, regex=url_regex))
                if not app in tech:
                    tech[app] = apps[app]

    for t in list(tech.keys()):
        for imply in tech[t].get('implies', []):
            print(imply, "detected because implied by", t)
            tech[imply] = apps[imply]

    for t in tech:
        tech[t]['category'] = categories[tech[t]['cats'][0]]['name']

    for t in list(tech.keys()):
        for exclude in tech[t].get('excludes', []):
            print("removing", exclude)
            del(tech[t])

    pprint(tech)



def search(domain):
    q="site:{}".format(domain)

    server = "www.google.com"
    userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"

    headers = {
        'Host': server,
        'Cookie': 'SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50',
        'User-Agent': userAgent,
        'Accept-Language': 'en-us,en',
    }

    for counter in range(5):

        url = "https://" + server + "/search?&start=" + str(counter) + "&hl=en&meta=&q=%40\"" + q + "\""
        r = requests.get(url, headers=headers)
        #returncode, returnmsg, headers = h.getreply()
        #self.results = h.getfile().read()
        results = r.text
        soup = BeautifulSoup(results, 'html.parser')
        for a in soup.find_all('a'):
            if a['href'].startswith('/url?q='):
                url = a['href']
                url = url.split('&')[0].replace('/url?q=', '')
                #url = url.split('/')[2]

                print(url)
                #if 'Perfil profesional' in a.text:
                #    linkedin_url = a['href'].split('&')[0].replace('/url?q=', '')
                #    name = a.text.split('|')[0].strip()
                #    print(email, name, linkedin_url)
                #    return { 'name': name, 'linkedin_url': linkedin_url }
                #    break
    return None
    #pprint(results)


if __name__ == '__main__':
    cmd_weburls()

#!/usr/bin/env python3

import json
import logging
import os
import os.path
import pwd
import webbrowser

import click
import requests
import requests_cache

from habu.lib.loadcfg import loadcfg

urls = {
    'aboutme': 'https://about.me/{}',
    'angelist': 'https://angel.co/{}',
    'asciinema': 'https://asciinema.org/~{}',
    'badoo': 'https://badoo.com/en/profile/{}',
    'bandcamp': 'https://bandcamp.com/{}',
    'basecamp': 'https://{}.basecamphq.com/login',
    'behance': 'https://www.behance.net/{}',
    'bitbucket': 'https://bitbucket.org/{}/',
    'bitly': 'https://bitly.com/u/{}',
    'blogger': 'http://{}.blogspot.com/',
    'cashme': 'https://cash.me/$hey{}/',
    'codeacademy': 'https://www.codecademy.com/{}',
    'codementor': 'https://www.codementor.io/{}',
    'dailymotion': 'https://www.dailymotion.com/{}',
    'devianart': 'https://{}.devianart.com/',
    'disqus': 'https://disqus.com/by/{}/',
    'dribble': 'https://dribbble.com/{}',
    'etsy': 'https://www.etsy.com/people/{}',
    'facebook': 'https://www.facebook.com/{}',
    'fanpop': 'http://www.fanpop.com/fans/{}',
    'fiverr': 'https://www.fiverr.com/{}',
    'fotolog': 'https://fotolog.com/{}/',
    'flickr': 'https://www.flickr.com/photos/{}/',
    'github': 'https://github.com/{}/',
    'goodread': 'https://www.goodreads.com/{}',
    'googleplus': 'https://plus.google.com/+{}/posts',
    'hubpages': 'https://hubpages.com/@{}',
    'imgur': 'https://imgur.com/user/{}',
    'ifttt': 'https://ifttt.com/p/{}',
    'instagram': 'https://instagram.com/{}/',
    'instructables': 'https://www.instructables.com/member/{}/',
    'keybase': 'https://keybase.io/{}',
    'kongregate': 'http://www.kongregate.com/accounts/{}',
    'lastfm': 'https://www.last.fm/user/{}',
    'livejournal': 'https://{}.livejournal.com/',
    'medium': 'https://medium.com/@{}',
    'mercadolibre': 'https://perfil.mercadolibre.com.ar/{}',
    'openhub': 'https://www.openhub.net/accounts/{}',
    'pastebin': 'https://pastebin.com/u/{}',
    'pinterest': 'https://in.pinterest.com/{}/',
    'producthunt': 'https://www.producthunt.com/@{}',
    'quora': 'https://{}.quora.com/',
    'reddit': 'https://www.reddit.com/user/{}/',
    'slack': 'https://{}.slack.com/',
    'slideshare': 'https://www.slideshare.net/{}',
    'soundcloud': 'https://soundcloud.com/{}',
    'soup': 'http://{}.soup.io/',
    'tripadvisor': 'https://www.tripadvisor.com/members/{}',
    'tumblr': 'https://{}.tumblr.com',
    'twitter': 'https://twitter.com/{}',
    'vimeo': 'https://vimeo.com/{}',
    'vk': 'http://vk.com/{}',
    'wikipedia': 'https://en.wikipedia.org/wiki/User:{}',
    'wordpress': 'https://{}.wordpress.com/',
    'youtube':'https://www.youtube.com/{}',
}


@click.command()
@click.argument('username')
@click.option('-c', 'no_cache', is_flag=True, default=False, help='Disable cache')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-w', 'wopen', is_flag=True, default=False, help='Open each valid url in a webbrowser')
def cmd_usercheck(username, no_cache, verbose, wopen):
    """Check if the given username exists on various social networks and other popular sites.

    \b
    $ habu.usercheck portantier
    {
        "aboutme": "https://about.me/portantier",
        "disqus": "https://disqus.com/by/portantier/",
        "github": "https://github.com/portantier/",
        "ifttt": "https://ifttt.com/p/portantier",
        "lastfm": "https://www.last.fm/user/portantier",
        "medium": "https://medium.com/@portantier",
        "pastebin": "https://pastebin.com/u/portantier",
        "pinterest": "https://in.pinterest.com/portantier/",
        "twitter": "https://twitter.com/portantier",
        "vimeo": "https://vimeo.com/portantier"
    }
    """

    habucfg = loadcfg()

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if not no_cache:
        homedir = pwd.getpwuid(os.getuid()).pw_dir
        requests_cache.install_cache(homedir + '/.habu_requests_cache')
        logging.info('using cache on ' + homedir + '/.habu_requests_cache')

    existent = {}

    for site, url in urls.items():
        u = url.format(username)
        logging.info(u)
        try:
            r = requests.head(u, allow_redirects=False)
        except Exception:
            continue
        if r.status_code == 200:
            if requests.head(url.format('zei4fee3q9'), allow_redirects=False).status_code == 200:
                logging.error('Received status 200 for user zei4fee3q9, maybe, the check needs to be fixed')
            else:
                existent[site] = u
                if wopen:
                    webbrowser.open_new_tab(u)

    print(json.dumps(existent, indent=4))

if __name__ == '__main__':
    cmd_usercheck()

#!/usr/bin/env python3

import base64
import json
from pathlib import Path
import logging
import click
import pwd
import os
import requests
from Crypto import Random
from Crypto.Hash import SHA224
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


@click.command()
@click.option('-u', 'url', default='https://asydns.org', help='API URL')
@click.option('-g', 'generate', is_flag=True, default=False, help='Force the generation of a new key pair')
@click.option('-r', 'revoke', is_flag=True, default=False, help='Revoke the public key')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_asydns(url, generate, revoke, verbose):
    """Requests a DNS domain name based on public and private
    RSA keys using the AsyDNS protocol https://github.com/portantier/asydns

    Example:

    \b
    $ habu.asydns -v
    Generating RSA key ...
    Loading RSA key ...
    {
        "ip": "181.31.41.231",
        "name": "07286e90fd6e7e6be61d6a7919967c7cf3bbfb23a36edbc72b6d7c53.a.asydns.org"
    }

    \b
    $ dig +short 07286e90fd6e7e6be61d6a7919967c7cf3bbfb23a36edbc72b6d7c53.a.asydns.org
    181.31.41.231
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    homedir = Path(pwd.getpwuid(os.getuid()).pw_dir)

    dotdir = homedir / '.asydns'
    dotdir.mkdir(exist_ok=True)

    pub_file = dotdir / 'rsa.pub'
    key_file = dotdir / 'rsa.key'

    if generate or not key_file.is_file():

        logging.info('Generating RSA key ...')
        random_generator = Random.new().read
        key = RSA.generate(2048, random_generator)
        pub = key.publickey()

        with key_file.open('w') as k:
            k.write(key.exportKey('PEM').decode())

        with pub_file.open('w') as p:
            p.write(pub.exportKey('PEM').decode())


    logging.info('Loading RSA key ...')
    with key_file.open() as k:
        key = RSA.importKey(k.read())

    with pub_file.open() as p:
        pub = RSA.importKey(p.read())


    r = requests.get(url + '/api')

    if r.status_code != 200:
        logging.error('Error')
        logging.error(r.content.decode())
        return False

    j = r.json()

    challenge = base64.b64decode(j['challenge'])
    signer = PKCS1_v1_5.new(key)
    response = signer.sign(SHA224.new(challenge))
    response = base64.b64encode(response).decode()

    if revoke:
        r = requests.delete(url + '/api', json={'pub': pub.exportKey('PEM').decode(), 'challenge' : j['challenge'], 'response': response})
    else:
        r = requests.post(url + '/api', json={'pub': pub.exportKey('PEM').decode(), 'challenge' : j['challenge'], 'response': response})

    if r.status_code != 200:
        logging.error('Error')
        logging.error(r.content.decode())
        return False

    print(json.dumps(r.json(), indent=4))

    return True

if __name__ == '__main__':
    cmd_asydns()


#!/usr/bin/env python3

import base64
import json
import logging
import os
import os.path
from pathlib import Path

import click
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


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

    #homedir = Path(pwd.getpwuid(os.getuid()).pw_dir)
    homedir = Path(os.path.expanduser('~'))

    dotdir = homedir / '.asydns'
    dotdir.mkdir(exist_ok=True)

    pub_file = dotdir / 'rsa.pub'
    key_file = dotdir / 'rsa.key'

    if generate or not key_file.is_file():

        logging.info('Generating RSA key ...')

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        pub = key.public_key()

        key_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pub_key = pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with key_file.open('w') as k:
            k.write(key_pem.decode())

        with pub_file.open('w') as p:
            p.write(pub_key.decode())


    logging.info('Loading RSA key ...')

    with key_file.open("rb") as key_file:
        key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    with pub_file.open("r") as pub_file:
        pub_pem = pub_file.read()

    r = requests.get(url + '/api')

    if r.status_code != 200:
        logging.error('Error')
        logging.error(r.content.decode())
        return False

    j = r.json()

    challenge = base64.b64decode(j['challenge'])

    response = key.sign(
        challenge,
        padding.PKCS1v15(
        ),
        hashes.SHA224()
    )

    response = base64.b64encode(response).decode()

    if revoke:
        r = requests.delete(url + '/api', json={'pub': pub_pem, 'challenge' : j['challenge'], 'response': response})
    else:
        r = requests.post(url + '/api', json={'pub': pub_pem, 'challenge' : j['challenge'], 'response': response})

    if r.status_code != 200:
        logging.error('Error')
        logging.error(r.content.decode())
        return False

    print(json.dumps(r.json(), indent=4))

    return True

if __name__ == '__main__':
    cmd_asydns()

#!/usr/bin/env python3

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509 import Extensions

from pprint import pprint


def certclone(chain, copy_extensions=False):

    for i in range(len(chain)):
        chain[i] = chain[i].to_cryptography()

    newchain = []

    '''
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        )

    pubkey = key.public_key()
    '''

    first = True

    for original in chain[::-1]:

        #print(cert)

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
            )

        key_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        if first:
            print(key_pem)
            first=False

        pubkey = key.public_key()

        # Todo: Code to mimic the private key type of original cert
        # maybe based on pubkey.__class__
        cert = x509.CertificateBuilder()
        cert = cert.subject_name(original.subject)
        cert = cert.issuer_name(original.issuer)
        #cert = cert.serial_number(original.serial_number)
        cert = cert.serial_number(x509.random_serial_number())
        cert = cert.not_valid_before(original.not_valid_before)
        cert = cert.not_valid_after(original.not_valid_after)
        cert = cert.public_key(pubkey)

        if copy_extensions:
            for ext in original.extensions:
                cert = cert.add_extension(ext.value, critical=ext.critical)

        cert = cert.sign(private_key=key, algorithm=original.signature_hash_algorithm, backend=default_backend())
        cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode()
        print(cert_pem)

        newchain.insert(0, cert)

    #pprint(newchain)
    #return (key_pem, cert_pem)


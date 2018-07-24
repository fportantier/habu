#!/usr/bin/env python3

from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509 import Extensions


def certclone(cert_data, copy_extensions=False, expired=False):

    try:
        original = x509.load_pem_x509_certificate(cert_data, default_backend())
    except ValueError:
        pass

    try:
        original = x509.load_der_x509_certificate(cert_data, default_backend())
    except ValueError:
        raise ValueError("No recognized cert format. Allowed: PEM or DER")

    pubkey = original.public_key()

    # Todo: Code to mimic the private key type of original cert
    # maybe based on pubkey.__class__
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        )

    cert = x509.CertificateBuilder()
    cert = cert.subject_name(original.subject)
    cert = cert.issuer_name(original.issuer)
    cert = cert.serial_number(original.serial_number)
    cert = cert.not_valid_before(original.not_valid_before)

    if expired:
        cert = cert.not_valid_after(datetime.now() - timedelta(days=1))
    else:
        cert = cert.not_valid_after(original.not_valid_after)

    cert = cert.public_key(key.public_key())

    if copy_extensions:
        for ext in original.extensions:
            cert = cert.add_extension(ext.value, critical=ext.critical)

    cert = cert.sign(private_key=key, algorithm=original.signature_hash_algorithm, backend=default_backend())

    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode()

    return (key_pem, cert_pem)


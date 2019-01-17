#!/usr/bin/env python3

from base64 import b64decode
from binascii import unhexlify

import click
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


@click.command()
@click.argument('password')
def decrypt_gpp(password):

    """
    Decrypt the password of local users added via Windows 2008 Group Policy Preferences.

    This value is the 'cpassword' attribute embedded in the Groups.xml file, stored in the domain controller's Sysvol share.

    Example:

    \b
    # habu.decrypt.gpp AzVJmXh/J9KrU5n0czX1uBPLSUjzFE8j7dOltPD8tLk
    testpassword
    """

    iv = b"\x00" * 16

    # add the '=' characters for padding, if needed
    password += "=" * ((4 - len(password) % 4) % 4)
    password = b64decode(password)

    key = """
    4e 99 06 e8  fc b6 6c c9  fa f4 93 10  62 0f fe e8
    f4 96 e8 06  cc 05 79 90  20 9b 09 a4  33 b6 6c 1b
    """.replace(" ","").replace("\n","")

    key = unhexlify(key)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plain = decryptor.update(password) + decryptor.finalize()

    print(plain.decode(errors='ignore'))


if __name__ == '__main__':
    decrypt_gpp()

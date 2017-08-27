
from habu.lib.xor import xor


def test_xor():
    text = b'text to encrypt'
    encrypted = xor(text)
    assert text == xor(encrypted)


def test_xor_w_key():
    text = b'text to encrypt'
    key = b'secret'
    encrypted = xor(text, key)
    assert text == xor(encrypted, key)


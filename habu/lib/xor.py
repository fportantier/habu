from itertools import cycle


def xor(a, b='0'.encode()):

    return bytes([a ^ b for a, b in zip(a, cycle(b))])


if __name__ == '__main__':
    text = b'text to encrypt'
    encrypted = xor(text)
    plain = xor(encrypted)
    print(text == plain)

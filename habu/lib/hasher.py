import hashlib

ALGOS = [
    'md5',
    'sha1',
    'sha512',
    'ripemd160',
    'whirlpool',
]


def hasher(data, algos=ALGOS):

    try:
        data = data.encode()
    except Exception:
        pass

    result = {}

    for algo in sorted(hashlib.algorithms_available):
        if algo in algos:
            h = hashlib.new(algo)
            h.update(data)
            result[algo] = h.hexdigest()

    return result


if __name__ == '__main__':
    from pprint import pprint
    pprint(hasher('password'))


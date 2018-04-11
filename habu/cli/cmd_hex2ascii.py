import codecs

import click


@click.command()
@click.argument('f', type=click.File('r'))
def cmd_hex2ascii(f):

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    data = data.replace(' ', '')
    data = data.replace('\n', '')

    decoded = codecs.decode(data, "hex")

    print(decoded.decode("utf-8", errors='ignore'))


if __name__ == '__main__':
    cmd_hex2ascii()

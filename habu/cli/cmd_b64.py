import base64
import sys

import click


@click.command()
@click.argument('f', type=click.File('rb'))
@click.option('-d', 'do_decode', is_flag=True, default=False, help='decode instead of encode')
def cmd_b64(f, do_decode):

    print("WARNING: This tool has problems decoding b64 data.", file=sys.stderr)

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    #decoded = codecs.decode(data, "hex")

    if do_decode:
        print(base64.b64decode(data), file=sys.stdout)
    else:
        print(base64.b64encode(data).decode())


if __name__ == '__main__':
    cmd_b64()

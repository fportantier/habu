import click

from habu.lib.xor import xor


@click.command()
@click.option('-k', default='0', help='Encryption key')
@click.option('-i', type=click.File('rb'), required=True, help='Input file')
@click.option('-o', type=click.File('wb'), required=True, help='Output file')
def cmd_xor(k, i, o):
    """XOR cipher"""
    o.write(xor(i.read(), k.encode()))


if __name__ == '__main__':
    cmd_xor()

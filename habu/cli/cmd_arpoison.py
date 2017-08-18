import click
from habu.lib.arpoison import arpoison


@click.command()
@click.argument('target1')
@click.argument('target2')
def cmd_arpoison(target1, target2):
    """ARP cache poison"""
    arpoison(target1, target2)

if __name__ == '__main__':
    cmd_arpoison()

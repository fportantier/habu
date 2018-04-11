import click

from habu.lib.eicar import eicar


@click.command()
def cmd_eicar():
    """EICAR test data"""
    print(eicar())

if __name__ == '__main__':
    cmd_eicar()

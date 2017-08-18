import click
from habu.lib.ip import get_ip


@click.command()
def cmd_ip():
    """Example script."""
    print(get_ip())

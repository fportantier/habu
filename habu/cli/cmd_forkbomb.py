import click

from habu.lib.forkbomb import bombs, get_bomb


@click.command()
@click.argument('bomb', type=click.Choice(bombs))
def cmd_forkbomb(bomb):
    """Fork Bombs"""
    print(get_bomb(bomb))


if __name__ == '__main__':
    cmd_forkbomb()

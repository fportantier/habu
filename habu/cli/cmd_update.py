import click

import habu.lib.manuf


@click.command()
def cmd_update():
    """ Data files updater """
    m = habu.lib.manuf.MacParser()
    m.update()

if __name__ == '__main__':
    cmd_update()

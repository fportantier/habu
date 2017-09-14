import click
from habu.lib.hasher import hasher



@click.command()
@click.argument('f', type=click.File('rb'))
def cmd_hasher(f):
    """Hasher"""

    data = f.read()

    if not data:
        print("Empty file or string!")
    else:
        for algo, result in hasher(data).items():
            print("{:<12}: {}".format(algo, result))

if __name__ == '__main__':
    cmd_hasher()

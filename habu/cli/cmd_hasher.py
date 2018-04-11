import click

from habu.lib.hasher import ALGOS, hasher


@click.command()
@click.argument('f', type=click.File('rb'))
@click.option('-a', 'algorithm', default=None, type=click.Choice(ALGOS), help='Only this algorithm (Default: all)')
def cmd_hasher(f, algorithm):
    """Hasher"""

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    if algorithm:
        print(hasher(data, algorithm)[algorithm])
    else:
        for algo, result in hasher(data).items():
            print("{:<12}: {}".format(algo, result))

if __name__ == '__main__':
    cmd_hasher()

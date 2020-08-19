import logging
import os
from pathlib import Path

import click
import pkg_resources


def find_console_scripts(package_name):
    entrypoints = [ ep.name for ep in pkg_resources.iter_entry_points('console_scripts') if ep.module_name.startswith(package_name) ]
    return entrypoints


@click.command()
def cmd_clean():
    """Clean old habu entrypoints."""

    logging.basicConfig(level=logging.INFO)

    entrypoints = find_console_scripts('habu')

    for dirname in os.environ['PATH'].split(':'):
        for filename in Path(dirname).glob('habu.*'):
            if filename.name not in entrypoints:
                try:
                    filename.unlink()
                    logging.info(f'Deleted entrypoint {filename}')
                except Exception as e:
                    logging.error(f'Error deleting {filename}: {e}')


if __name__ == '__main__':
    cmd_clean()

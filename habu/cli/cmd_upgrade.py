import logging
import os
import subprocess
from pathlib import Path

import click
import pkg_resources


def find_console_scripts(package_name):
    entrypoints = [ ep.name for ep in pkg_resources.iter_entry_points('console_scripts') if ep.module_name.startswith(package_name) ]
    return entrypoints


def clean_old_entrypoints():
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


@click.command()
def cmd_upgrade():
    """Upgrade habu (from https://github.com/fportantier/habu)"""

    logging.basicConfig(level=logging.INFO)

    command = [
        'python3',
        '-m',
        'pip',
        'install',
        '--upgrade',
        'git+https://github.com/fportantier/habu.git'
    ]

    p = subprocess.Popen(command)
    p.wait()

    clean_old_entrypoints()

if __name__ == '__main__':
    cmd_upgrade()

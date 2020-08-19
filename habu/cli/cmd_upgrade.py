import logging
import subprocess

import click


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

    p = subprocess.Popen(['habu.clean'])
    p.wait()


if __name__ == '__main__':
    cmd_upgrade()

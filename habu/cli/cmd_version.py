#!/usr/bin/env python3

import click
import pkg_resources


@click.command()
def cmd_version():
    print(pkg_resources.get_distribution("habu").version)


if __name__ == "__main__":
    cmd_version()

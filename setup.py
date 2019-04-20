#!/usr/bin/env python3
"""Habu Python Wrapper setup script."""
import os
import sys
import glob

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

entries = []

for file in sorted(glob.glob("habu/cli/cmd_*.py")):
    cmd_file = file.replace('habu/cli/', '').replace('.py', '')
    cmd_name = cmd_file.replace('cmd_', 'habu.').replace('_', '.')
    entries.append("{cmd_name} = habu.cli.{cmd_file}:{cmd_file}".format(cmd_file=cmd_file, cmd_name=cmd_name))

setup(
    name='habu',
    version='0.1.7',
    description='Python Network Hacking Toolkit',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Fabian Martinez Portantier',
    author_email='fabian@portantier.com',
    url='https://github.com/portantier/habu',
    license='BSD 3-clause',
    install_requires=[
        'beautifulsoup4',
        'cryptography',
        'click',
        'dnspython',
        'lxml',
        'netifaces',
        #'prompt_toolkit==1.0.15',
        'pycrypto',
        'pygments',
        'regex',
        'requests',
        'requests-cache',
        'scapy',
        'websockets',
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': entries,
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['habu', 'habu.lib', 'habu.lib.completeme', 'habu.cli'],
    include_package_data=True,
    keywords=['security'],
    zip_safe=False,
    test_suite='py.test',
)

#!/bin/sh

python3 setup.py sdist
rm -Rf deb_dist
py2dsc-deb dist/$(ls -1r dist | head -n 1)


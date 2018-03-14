#!/bin/sh

python3 setup.py sdist
rm -Rf deb_dist
#py2dsc-deb $(ls -1r dist/*.gz | head -n 1)
python setup.py --command-packages=stdeb.command bdist_deb

#!/bin/sh

# Fix the readme problem - Step 1
mv README.md README.mda
sed -i s/README.md/README.txt/g setup.py

# Main work
python3 setup.py sdist
rm -Rf deb_dist
python setup.py --command-packages=stdeb.command bdist_deb

# Fix the readme problem - Step 2
mv README.mda README.md
sed -i s/README.txt/README.md/g setup.py


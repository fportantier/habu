#!/bin/sh

# Fix the readme problem - Step 1
mv README.md README.mda
sed -i s/README.md/README.txt/g setup.py

# Main work
python setup.py sdist upload --sign --identity fabian@portantier.com

# Fix the readme problem - Step 2
mv README.mda README.md
sed -i s/README.txt/README.md/g setup.py


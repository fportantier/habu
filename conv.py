from pathlib import Path
from m2r import parse_from_file

ifile = Path('README.md')
ofile = Path('README.rst')

readme_rst = parse_from_file(ifile)

with ofile.open('w') as outfile:
    outfile.write(readme_rst)



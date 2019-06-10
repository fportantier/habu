import os
import os.path
from pathlib import Path
import json
import sys

def loadcfg(environment=True):

    cfg = {}

    homedir = Path(os.path.expanduser('~'))
    cfgfile = homedir / '.habu.json'

    if cfgfile.is_file():
        #print('file exists!')
        with cfgfile.open() as f:
            try:
                cfg = json.loads(f.read())
            except Exception as e:
                pass

    if environment:
        for k,v in os.environ.items():
            if k.startswith('HABU_'):
                k = k.replace('HABU_', '')
                cfg[k] = v
                #print(k,v)


    cfg['BASEDIR'] = (Path(os.path.dirname(os.path.abspath(__file__))) / '..').resolve()
    cfg['DATADIR'] = Path(cfg['BASEDIR'] / 'data')

    return cfg

if __name__ == '__main__':
    loadcfg()


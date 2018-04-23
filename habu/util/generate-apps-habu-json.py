import json
import os
import os.path
from pathlib import Path

DATADIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))

def gahj():

    with (DATADIR / 'apps.json').open() as f:
        data = json.load(f)

    with (DATADIR / 'apps-custom.json').open() as f:
        data_custom = json.load(f)

    apps = data['apps']
    categories = data['categories']

    apps.update(data_custom['apps'])
    categories.update(data_custom['categories'])

    # convertir los strings a listas, para que siempre los valores sean listas
    for app in apps:
        for field in ['url', 'html', 'env', 'script', 'implies', 'excludes']:

            if field in apps[app]:
                if not isinstance(apps[app][field], list):
                    apps[app][field] = [apps[app][field]]

    with (DATADIR / 'apps-habu.json').open('w') as f:
        f.write(json.dumps({'apps':apps, 'categories': categories}, indent=4)) #data_custom = json.load(f)

if __name__ == '__main__':
    gahj()

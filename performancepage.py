import os
import json
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader


PATH = os.getcwd()

with open('conf.yml', 'r') as f:
    string = f.read()
    conf = yaml.load(string)


def output_html(text):
    if not os.path.isdir(os.path.join(PATH, 'output')):
        os.makedirs(os.path.join(PATH, 'output'))

    with open('output/index.html', 'w') as f:
        f.write(text)


def copy_assets(files):
    """takes a list of files or directories and copies to output
    """
    for f in files:
        if os.path.isdir(os.path.join(PATH, f)):
            try:
                shutil.copytree(os.path.join(PATH, f), os.path.join(PATH, 'output', f))
            except OSError:
                shutil.rmtree(os.path.join(PATH, 'output', f))
                shutil.copytree(os.path.join(PATH, f), os.path.join(PATH, 'output', f))
        else:
            shutil.copy(os.path.join(PATH, f), os.path.join(PATH, 'output', f))

def get_data(token, conf):
    pass

# Metrics grouped together.
# First in group get special treatment.

if __name__ == '__main__':
    dev = True
    if not dev:
        try:
            token = os.env['SD_TOKEN']
        except KeyError:
            raise KeyError('There needs to be an environment variable called SD_TOKEN')
        data = get_data(token, conf)
    else:
        data = {}

    env = Environment(
        loader=FileSystemLoader('templates')
    )
    template = env.get_template('index.html')
    data = {'general': conf['general'], 'infrastructure': conf['infrastructure']}
    html = template.render(templates_folder='templates', **data)
    output_html(html)

    assets = ['css', 'js', 'images']
    copy_assets(assets)

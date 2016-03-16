import os
import json
import shutil
import codecs

import yaml
from jinja2 import Environment, FileSystemLoader

from datawrapper import DataWrapper

PATH = os.getcwd()

with open('conf.yml', 'r') as f:
    string = f.read()
    conf = yaml.load(string)


def round_with_letter(value, letter):
    return "{} {}".format(int(value), letter)

def access_token_file(method, value=None):
    """method, either reading or writing"""
    try:
        token = os.environ['SD_AUTH_TOKEN']
        return token
    except KeyError:
        pass

    with codecs.open('.token', method) as f:
        if method == 'r':
            return f.read().strip()
        elif method == 'w':
            f.write(value)
        else:
            raise Exception('Only accepts "r" or "w"')

def output_html(text):
    if not os.path.isdir(os.path.join(PATH, 'output')):
        os.makedirs(os.path.join(PATH, 'output'))

    with codecs.open('output/index.html', 'w', encoding='utf8') as f:
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
            token = access_token_file('r')
        except IOError:
            token = raw_input('What is your token for Server Density: ').strip()
            access_token_file('w', token)
        data_container = DataWrapper(token, conf)
        data_container.gather_data()
        data = data_container.conf
        data['historic_data'] = data_container.historic_data
    else:
        # open a dev conf file that you can play around with
        with codecs.open('conf_dev.yml', 'r') as f:
            conf = yaml.load(f.read())
        data = conf

    env = Environment(
        loader=FileSystemLoader('templates')
    )
    env.filters['round_with_letter'] = round_with_letter
    template = env.get_template('index.html')
    html = template.render(templates_folder='templates', **data)
    output_html(html)

    assets = ['css', 'js', 'images']
    copy_assets(assets)

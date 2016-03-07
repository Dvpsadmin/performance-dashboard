import yaml
import json

with open('conf.yml', 'r') as f:
    string = f.read()
    conf = yaml.load(string)


# Metrics grouped together.
# First in group get special treatment.

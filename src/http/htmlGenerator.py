'''
Created on Sep 12, 2014

@author: ben
'''
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(["../media"]))

def generateHTML(uri, **kwargs):
    template = env.get_template(uri)
    result = template.render(**kwargs)
    return result.encode('utf-8')
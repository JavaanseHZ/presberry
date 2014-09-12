'''
Created on Sep 12, 2014

@author: ben
'''
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(["../media"]))

def generateHTML(self, uri, jinjaVars):
    template = env.get_template(uri)
    result = template.render(jinjaVars)
    print result.encode('utf-8')
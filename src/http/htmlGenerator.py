'''
Created on Sep 12, 2014

@author: ben
'''
import util.config as PRES_CONFIG
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader([PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML)]))

def generateHTML(uri, **kwargs):
    template = env.get_template(uri)
    result = template.render(**kwargs)
    return result.encode('utf-8')
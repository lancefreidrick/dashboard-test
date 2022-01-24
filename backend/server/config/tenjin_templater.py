"""
Tenjin Template Engine Service
"""
import os
import tenjin

from server.config import environment

config = environment.config

__templater = None


def setup():
    global __templater
    template_path = os.path.join(config.root_dir, 'server/templates')
    __templater = tenjin.Engine(path=[template_path])


def get_templater():
    return __templater

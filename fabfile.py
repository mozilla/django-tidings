"""Creating standalone Django apps is a PITA because you're not in a project,
so you don't have a settings.py file. I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.

"""
import functools
import os

from fabric.api import local, cd
from fabric.contrib.project import rsync_project


local = functools.partial(local, capture=False)

NAME = os.path.basename(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_app.settings'
os.environ['PYTHONPATH'] += (':' if os.environ['PYTHONPATH'] else '') + ROOT


def doc(kind='html'):
    with cd('docs'):
        local('make clean %s' % kind)

def shell():
    local('django-admin.py shell')

def test():
    # Just calling nosetests results in SUPPORTS_TRANSACTIONS KeyErrors.
    local('test_app/manage.py test tidings')

def updoc():
    doc('dirhtml')
    rsync_project('p/%s' % NAME, 'docs/_build/dirhtml/', delete=True)

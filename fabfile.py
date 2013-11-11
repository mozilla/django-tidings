"""Creating standalone Django apps is a PITA because you're not in a project,
so you don't have a settings.py file. I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.

"""
import functools
import os

from fabric.api import local, cd


local = functools.partial(local, capture=False)

ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_app.settings'
os.environ['PYTHONPATH'] = (((os.environ['PYTHONPATH'] + ':') if
    os.environ.get('PYTHONPATH') else '') + ROOT)


def doc(kind='html'):
    """Build Sphinx docs.

    Requires Sphinx to be installed.

    """
    with cd('docs'):
        local('make clean %s' % kind)

def shell():
    local('django-admin.py shell')

def test():
    # Just calling nosetests results in SUPPORTS_TRANSACTIONS KeyErrors.
    local('test_app/manage.py test tidings')

def updoc():
    """Build Sphinx docs and upload them to packages.python.org.

    Requires Sphinx-PyPI-upload to be installed.

    """
    doc('html')
    local('python setup.py upload_sphinx --upload-dir=docs/_build/html')

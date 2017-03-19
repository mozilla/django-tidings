import re

from setuptools import setup, find_packages


def long_description():
    readme = open('README.rst').read()
    raw_changes = open('docs/changes.rst').read()
    # Hack symbol names out of Sphinx directives:
    changes = re.sub(r':[a-zA-Z]+:`[0-9a-zA-Z~_\.]+\.([^`]+)`',
                     r'``\1``',
                     raw_changes)
    return readme + '\n' + changes


setup(
    name='django-tidings',
    version='1.1',
    description='Framework for asynchronous email notifications from Django',
    long_description=long_description(),
    author='Erik Rose',
    author_email='erik@mozilla.com',
    license='BSD',
    packages=find_packages(exclude=['tests*', 'tests']),
    url='http://github.com/mozilla/django-tidings',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django',
        'celery>=3.1'
    ],
    keywords="django-tidings tidings email notifications",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)

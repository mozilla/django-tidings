import re

from setuptools import setup, find_packages


setup(
    name='django-tidings',
    version='0.4',
    description='Framework for asynchronous email notifications from Django',
    long_description=open('README.rst').read() + \
                     # Hack symbol names out of Sphinx directives:
                     re.sub(r':[a-zA-Z]+:`[0-9a-zA-Z~_\.]+\.([^`]+)`',
                            r'``\1``',
                            open('docs/changes.rst').read()),
    author='Erik Rose',
    author_email='erik@mozilla.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    url='http://github.com/erikrose/django-tidings',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django',
        'celery>=2.1.1'],
    tests_require=[
        'jingo',
        'fabric',
        'django-nose',
        'django-celery',
        'mock',
        'South'],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)

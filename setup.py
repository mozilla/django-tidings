from setuptools import setup, find_packages


setup(
    name='django-tidings',
    version='0.1',
    description='Framework for asynchronous email notifications from Django',
    long_description=open('README.rst').read(),
    author='Erik Rose',
    author_email='erik@mozilla.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    url='http://github.com/erikrose/django-tidings',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django',
        'jingo',
        'celery>=2.1.1'],
    tests_require=[
        'fabric',
        'django_nose',
        'djcelery',
        'mock'],
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

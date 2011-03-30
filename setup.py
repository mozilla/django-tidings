from setuptools import setup, find_packages


setup(
    name='django-tidings',
    version='0.1',
    description='Framework for asynchronous email notifications from Django',
    long_description=open('README.rst').read(),
    author='Erik Rose',
    author_email='erik@mozilla.com',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    url='http://github.com/erikrose/django-tidings',
    include_package_data=True,
    package_data={'tidings': ['README.rst']},
    zip_safe=False,
    install_requires=[
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
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)

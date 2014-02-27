=================
Development Notes
=================

Testing
=======

To run django-tidings' self tests, install Fabric, then run this::

  fab test

If you run into ImportErrors, make sure your ``PYTHONPATH`` is set
happily. Here's how I do it::

  PYTHONPATH=/Users/erose/Checkouts/kitsune/vendor/src/celery:/Users/erose/Checkouts/kitsune/vendor/packages/mock:/Users/erose/Checkouts/kitsune/vendor/src/django:/Users/erose/Checkouts/kitsune/vendor/src/kombu:/Users/erose/Checkouts/kitsune/vendor/src/django-celery fab test

You can also run all the tests with several different environment
combinations using `tox <http://tox.readthedocs.org/en/latest/>`_::

  $ pip install tox
  $ tox


Documentation
=============

To build the docs, install Sphinx >= 1.1, which you may have to pull out of hg
(1.1 introduces private method support in autodoc), and run this::

  fab doc

You can upload new docs to http://packages.python.org/django-tidings/ by
installing Sphinx-PyPI-upload and running this::

  fab updoc

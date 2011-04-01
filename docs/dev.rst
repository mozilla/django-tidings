=================
Development Notes
=================

Testing
=======

To run django-tidings' self tests, install Fabric, then run this::

  fab test

If you run into ImportErrors, make sure your ``PYTHONPATH`` is set happily.


Documentation
=============

To build the docs, install Sphinx >= 1.1, which you may have to pull out of hg
(1.1 introduces private method support in autodoc), and run this::

  fab doc

You can upload new docs to http://packages.python.org/django-tidings/ by
installing Sphinx-PyPI-upload and running this::

  fab updoc

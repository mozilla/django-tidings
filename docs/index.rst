==============
django-tidings
==============

django-tidings is a framework for sending email notifications to users who have
registered interest in certain events, such as the modification of some model
object. Used by support.mozilla.org_ and developer.mozilla.org_, it is
optimized for large-scale installations. Its features include...

* Asynchronous operation using the celery_ task queue
* De-duplication of notifications
* Association of subscriptions with either registered Django users or anonymous
  email addresses
* Optional confirmation of anonymous subscriptions
* Hook points for customizing any page drawn and any email sent

.. _support.mozilla.org: https://support.mozilla.org/en-US/
.. _developer.mozilla.org: https://developer.mozilla.org/en-US/
.. _celery: http://www.celeryproject.org/

Contents
========

.. toctree::
  :maxdepth: 2
  
  installation
  introduction
  settings
  views
  design
  dev
  changes
  reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Credits
=======
`Erik Rose`_ and `Paul Craciunoiu`_ developed django-tidings, replacing
a simpler progenitor written by the whole `support.mozilla.com team`_,
including `Ricky Rosario`_ and `James Socol`_.

`Will Kahn-Greene`_ worked on the 1.0 release. He updated the project to Django
1.4 through 1.6, added tox_ support to make multi-version testing easier, and
fixed bugs.

`Jannis Leidel`_ worked on the 1.1 release. He updated the project to Django 1.7
and 1.8, added South_ migrations, refactored tests, added TravisCI_ and
Coveralls_ support, switched from Fabric_ to a Makefile, switched from mock_ and
django_nose_ to Django tests, and more.

`John Whitlock`_ worked on the 1.2 and 2.0 releases. He added support for
Python 3 and Django 1.9 through 2.0. He added linting with flake8_, switched
from jingo_ to Django templates, and switched from django_celery_ to basic
Celery_.

.. _`Erik Rose`: https://github.com/erikrose
.. _`Paul Craciunoiu`: https://github.com/pcraciunoiu
.. _`Ricky Rosario`: https://github.com/rlr
.. _`James Socol`: https://github.com/jsocol
.. _`Will Kahn-Greene`: https://github.com/willkg
.. _`Jannis Leidel`: https://github.com/jezdez
.. _`John Whitlock`: https://github.com/jwhitlock
.. _`support.mozilla.com team`: https://github.com/mozilla/kitsune
.. _tox: https://tox.readthedocs.io/en/latest/
.. _South: http://south.aeracode.org/
.. _Fabric: http://www.fabfile.org/
.. _TravisCI: https://travis-ci.org/mozilla/django-tidings
.. _Coveralls: https://coveralls.io/github/mozilla/django-tidings
.. _mock: https://github.com/testing-cabal/mock
.. _django_nose: https://github.com/django-nose/django-nose
.. _flake8: http://flake8.pycqa.org/en/latest/
.. _jingo: https://github.com/jbalogh/jingo
.. _django_celery: https://github.com/celery/django-celery
.. _Celery: http://www.celeryproject.org/

.. Add your name if you commit something!

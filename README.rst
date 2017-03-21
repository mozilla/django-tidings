==============
django-tidings
==============

.. image:: https://img.shields.io/pypi/v/django-tidings.svg
   :target: https://pypi.python.org/pypi/django-tidings

.. image:: https://img.shields.io/travis/mozilla/django-tidings.svg
   :target: http://travis-ci.org/mozilla/django-tidings

.. image:: https://img.shields.io/coveralls/mozilla/django-tidings.svg
   :target: https://coveralls.io/github/mozilla/django-tidings

.. image:: https://readthedocs.org/projects/django-tidings/badge/
   :target: https://django-tidings.readthedocs.io/en/latest/

.. Omit badges from docs

django-tidings is a framework for sending email notifications to users who have
registered interest in certain events, such as the modification of some model
object. Used by support.mozilla.com, it is optimized for large-scale
installations. Its features include...

* Asynchronous operation using the ``celery`` task queue
* De-duplication of notifications
* Association of subscriptions with either registered Django users or anonymous
  email addresses
* Optional confirmation of anonymous subscriptions
* Hook points for customizing any page drawn and any email sent

Please see the full documentation at https://django-tidings.readthedocs.io/en/latest/

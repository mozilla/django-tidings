Version History
===============

1.2 (2017-03-22)
  * Added support for Django 1.8 and Python 3
  * Dropped support for Python 2.6

1.1 (2015-04-23)
  * Added support for Django 1.7
  * Dropped support for Django 1.4, 1.5 and 1.6
  * Dropped mock, Fabric and django-nose dependencies.
  * Moved tests outside of app and simplified test setup.
  * Added Travis CI: https://travis-ci.org/mozilla/django-tidings
  * Moved to ReadTheDocs: https://django-tidings.readthedocs.io/

1.0 (2015-03-03)
  * Support Django 1.6.
  * Fix a bug in reconstituting models under (perhaps) Django 1.5.x and up.
  * Remove rate limit on ``claim_watches`` task.
  * Add tox to support testing against multiple Django versions.

0.4
  * Fix a deprecated celery import path.
  * Add support for newer versions of Django, and drop support for older ones.
    We now support 1.4 and 1.5.
  * Add an initial South migration.

.. warning::

  If you're already using South in your project, you need to run the following
  command to create a "fake" migration step in South's migration history::

      python path/to/manage.py migrate tidings --fake

0.3
  * Support excluding multiple users when calling
    :meth:`~tidings.events.Event.fire()`.

0.2
  * API change: :meth:`~tidings.events.Event._mails()` now receives,
    in each user/watch tuple, a list of :class:`~tidings.models.Watch`
    objects rather than just a single one. This enables you to list all
    relevant watches in your emails or to make decisions from an
    :class:`~tidings.events.EventUnion`'s ``_mails()`` method based on
    what kind of events the user was subscribed to.
  * Expose a few attribute docs to Sphinx.

0.1
  * Initial release. In production on support.mozilla.com. API may change.

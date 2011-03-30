==============
django-tidings
==============

``django-tidings`` is a library for sending email notifications from a Django
app. It is optimized for large-scale installations, having features such as...

* Asynchronous sending using the ``celery`` task queue
* De-duplication of notifications
* Associating subscriptions with either registered Django users or anonymous
  email addresses
* Requiring confirmation of anonymous subscriptions (optional)
* Hook points for customizing any page it draws and any email it sends

Overview
========

To do: explain the concept of Events and their overlapping scoping rules.

Testing
=======

To run django-tidings' self tests, install Fabric, then run this::

  fab test

If you run into ImportErrors, make sure your ``PYTHONPATH`` is set happily.

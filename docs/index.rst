==============
django-tidings
==============

django-tidings is a framework for sending email notifications from a Django app
in response to arbitrary events such as the modification of some model object.
Used by support.mozilla.com, it is optimized for large-scale installations,
having features like...

* Asynchronous operation using the celery_ task queue
* De-duplication of notifications
* Association of subscriptions with either registered Django users or anonymous
  email addresses
* Optional confirmation of anonymous subscriptions
* Hook points for customizing any page drawn and any email sent

.. _celery: http://celeryproject.org/

Contents
========

.. toctree::
  :maxdepth: 2
  
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


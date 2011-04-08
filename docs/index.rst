==============
django-tidings
==============

django-tidings is a framework for sending email notifications to users who have
registered interest in certain events, such as the modification of some model
object. Used by support.mozilla.com, it is optimized for large-scale
installations. Its features include...

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

django-tidings was developed by Erik Rose and Paul Craciunoiu, replacing a
simpler progenitor written by the whole support.mozilla.com team, including
Ricky Rosario and James Socol.

.. Add your name if you commit something!

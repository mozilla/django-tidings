==============
django-tidings
==============

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

Please see the full documentation at http://packages.python.org/django-tidings/

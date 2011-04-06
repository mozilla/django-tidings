========
Settings
========

django-tidings offers several Django settings to customize its behavior:

.. module:: django.conf.settings

.. data:: TIDINGS_FROM_ADDRESS

  The address from which tidings' emails will appear to come. Most of the time,
  the :class:`~tidings.events.Event` has an opportunity to override this in
  code, but this setting is used as a default for conveniences like
  :func:`~tidings.utils.emails_with_users_and_watches` and the default
  implementation of :meth:`Event._activation_email()
  <tidings.events.Event._activation_email>`.
  
  Default: No default; you must set it manually.
  
  Example::
  
    TIDINGS_FROM_ADDRESS = 'notifications@example.com'

.. data:: TIDINGS_CONFIRM_ANONYMOUS_WATCHES

  A Boolean: whether to require email confirmation of anonymous watches. If
  this is ``True``, tidings will send a mail to the creator of an anonymous
  watch with a confirmation link. That link should point to a view which calls
  :meth:`Watch.activate() <tidings.models.Watch.activate>` and saves the watch.
  (No such built-in view is yet provided.) Until the watch is activated,
  tidings will ignore it.
  
  Default: No default; you must set it manually.
  
  Example::
  
    TIDINGS_CONFIRM_ANONYMOUS_WATCHES = True

.. data:: TIDINGS_MODEL_BASE

  A dotted path to a model base class to use instead of
  ``django.db.models.Model``. This can come in handy if, for example, you would
  like to add memcached support to tidings' models. To avoid staleness, tidings
  will use the ``uncached`` manager (if it exists) on its models when
  performing a staleness-sensitive operation like determining whether a user
  has a certain watch.
  
  Default: ``'django.db.models.Model'``
  
  Example::
    
    TIDINGS_MODEL_BASE = 'sumo.models.ModelBase'

.. data:: TIDINGS_REVERSE

  A dotted path to an alternate implementation of Django's ``reverse()``
  function. support.mozilla.com uses this to make tidings aware of the locale
  prefixes on its URLs, e.g. ``/en-US/unsubscribe``.
  
  Default: ``'django.core.urlresolvers.reverse'``
  
  Example::
    
    TIDINGS_REVERSE = 'sumo.urlresolvers.reverse'

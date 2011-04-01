============
Installation
============

To install django-tidings in your Django project, make these changes to ``settings.py``:

1. Add ``tidings`` to ``INSTALLED_APPS``::

     INSTALLED_APPS = [
       'other',
       'apps',
       'here',
       ...
       'tidings'
     ]

2. Define the settings :data:`~django.conf.settings.TIDINGS_FROM_ADDRESS` and
   :data:`~django.conf.settings.TIDINGS_CONFIRM_ANONYMOUS_WATCHES`.

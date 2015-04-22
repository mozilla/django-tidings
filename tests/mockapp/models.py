from django.db import models

from tidings.models import NotificationsMixin


# TODO: figure out why placing the mixin *after* models.Model fails
# See also http://code.djangoproject.com/ticket/10249
class MockModel(NotificationsMixin, models.Model):
    pass

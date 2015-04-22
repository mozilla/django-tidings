import random
from string import letters

from django.contrib.auth import get_user_model
from django.test import TestCase  # noqa

try:
    from django.test import override_settings  # noqa
except ImportError:
    from django.test.utils import override_settings  # noqa

from tidings.models import Watch, WatchFilter


def user(save=False, **kwargs):
    defaults = {'password':
                    'sha1$d0fcb$661bd5197214051ed4de6da4ecdabe17f5549c7c'}
    if 'username' not in kwargs:
        defaults['username'] = ''.join(random.choice(letters)
                                       for x in xrange(15))
    defaults.update(kwargs)
    u = get_user_model()(**defaults)
    if save:
        u.save()
    return u


def watch(save=False, **kwargs):
    # TODO: better defaults, when there are events available.
    defaults = {'user': kwargs.get('user') or user(),
                'is_active': True,
                'secret': 'abcdefghjk'}
    defaults.update(kwargs)
    w = Watch.objects.create(**defaults)
    if save:
        w.save()
    return w


def watch_filter(save=False, **kwargs):
    defaults = {'watch': kwargs.get('watch') or watch(),
                'name': 'test',
                'value': 1234}
    defaults.update(kwargs)
    f = WatchFilter.objects.create(**defaults)
    if save:
        f.save()
    return f

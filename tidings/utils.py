from zlib import crc32
from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.utils.six import next, string_types


def collate(*iterables, **kwargs):
    """Return an iterable ordered collation of the already-sorted items
    from each of ``iterables``, compared by kwarg ``key``.

    If ``reverse=True`` is passed, iterables must return their results in
    descending order rather than ascending.

    """
    key = kwargs.pop('key', lambda a: a)
    reverse = kwargs.pop('reverse', False)
    min_or_max = max if reverse else min

    rows = [iter(iterable) for iterable in iterables if iterable]
    next_values = {}
    by_key = []

    def gather_next_value(row, index):
        try:
            next_value = next(row)
        except StopIteration:
            pass
        else:
            next_values[index] = next_value
            by_key.append((key(next_value), index))

    for index, row in enumerate(rows):
        gather_next_value(row, index)

    while by_key:
        key_value, index = min_or_max(by_key)
        by_key.remove((key_value, index))
        next_value = next_values.pop(index)
        yield next_value
        gather_next_value(rows[index], index)


def hash_to_unsigned(data):
    """If ``data`` is a string or unicode string, return an unsigned 4-byte int
    hash of it. If ``data`` is already an int that fits those parameters,
    return it verbatim.

    If ``data`` is an int outside that range, behavior is undefined at the
    moment. We rely on the ``PositiveIntegerField`` on
    :class:`~tidings.models.WatchFilter` to scream if the int is too long for
    the field.

    We use CRC32 to do the hashing. Though CRC32 is not a good general-purpose
    hash function, it has no collisions on a dictionary of 38,470 English
    words, which should be fine for the small sets that :class:`WatchFilters
    <tidings.models.WatchFilter>` are designed to enumerate. As a bonus, it is
    fast and available as a built-in function in some DBs. If your set of
    filter values is very large or has different CRC32 distribution properties
    than English words, you might want to do your own hashing in your
    :class:`~tidings.events.Event` subclass and pass ints when specifying
    filter values.

    """
    if isinstance(data, string_types):
        # Return a CRC32 value identical across Python versions and platforms
        # by stripping the sign bit as on
        # http://docs.python.org/library/zlib.html.
        return crc32(data.encode('utf-8')) & 0xffffffff
    else:
        return int(data)


def emails_with_users_and_watches(
        subject, template_path, vars, users_and_watches,
        from_email=settings.TIDINGS_FROM_ADDRESS, **extra_kwargs):
    """Return iterable of EmailMessages with user and watch values substituted.

    A convenience function for generating emails by repeatedly rendering a
    Django template with the given ``vars`` plus a ``user`` and ``watches`` key
    for each pair in ``users_and_watches``

    :arg template_path: path to template file
    :arg vars: a map which becomes the Context passed in to the template
    :arg extra_kwargs: additional kwargs to pass into EmailMessage constructor

    """
    template = loader.get_template(template_path)
    context = Context(vars)
    for u, w in users_and_watches:
        context['user'] = u

        # Arbitrary single watch for compatibility with 0.1
        # TODO: remove.
        context['watch'] = w[0]

        context['watches'] = w
        yield EmailMessage(subject,
                           template.render(context),
                           from_email,
                           [u.email],
                           **extra_kwargs)


def _imported_symbol(import_path):
    """Resolve a dotted path into a symbol, and return that.

    For example...

    >>> _imported_symbol('django.db.models.Model')
    <class 'django.db.models.base.Model'>

    Raise ImportError is there's no such module, AttributeError if no such
    symbol.

    """
    module_name, symbol_name = import_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, symbol_name)


def import_from_setting(setting_name, fallback):
    """Return the resolution of an import path stored in a Django setting.

    :arg setting_name: The name of the setting holding the import path
    :arg fallback: An import path to use if the given setting doesn't exist

    Raise ImproperlyConfigured if a path is given that can't be resolved.

    """
    path = getattr(settings, setting_name, fallback)
    try:
        return _imported_symbol(path)
    except (ImportError, AttributeError, ValueError):
        raise ImproperlyConfigured('No such module or attribute: %s' % path)


# Here to be imported by others:
reverse = import_from_setting('TIDINGS_REVERSE',
                              'django.core.urlresolvers.reverse')

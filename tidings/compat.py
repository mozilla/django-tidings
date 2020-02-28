"""Compatibility functions for tidings."""

# Python 2/3 compatibility for Django 1.11
try:
    # Django 2.2 and earlier include six, but it is only
    # needed for Python 2.7 under Django 1.11.
    from django.utils.six import (iteritems, iterkeys, string_types, next,
                                  text_type)
    from django.utils.six.moves import range, reduce
except ImportError:
    # Django 3.0 drops the six library, but only runs under Python 3
    # Copy Python 3 variants from https://github.com/benjaminp/six

    from functools import reduce
    assert reduce  # Make flake8 happier

    def iteritems(d, **kw):
        return iter(d.items(**kw))

    def iterkeys(d, **kw):
        return iter(d.keys(**kw))

    string_types = str,
    text_type = str

    # Asign built-ins to importable variables
    next = next
    range = range

# Python 3.3 deprecated importing ABCs from collections
# Since we still support Python 2.7, we need this indirection
try:
    from collections.abc import Sequence  # noqa: F401
except ImportError:
    from collections import Sequence  # noqa: F401

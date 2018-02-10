"""Compatibility functions for tidings."""

# The standard Django reverse function
# This is the default value if TIDINGS_REVERSE is not set
try:
    # Django 1.10 and later
    from django.urls import reverse
except ImportError:
    # Django 1.9 and earlier
    from django.core.urlresolvers import reverse
assert reverse


def is_authenticated(user):
    """Is a user instance authenticated?"""
    if callable(user.is_authenticated):
        # Django 1.9 and earlier
        return user.is_authenticated()
    else:
        # Django 1.10 and later
        return user.is_authenticated

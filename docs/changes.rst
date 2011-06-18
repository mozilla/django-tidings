Version History
===============

0.2
  * API change: :meth:`~tidings.events.Event._mails()` now receives,
    in each user/watch tuple, a list of :class:`~tidings.models.Watch`
    objects rather than just a single one. This enables you to list all
    relevant watches in your emails or to make decisions from an
    :class:`~tidings.events.EventUnion`'s ``_mails()`` method based on
    what kind of events the user was subscribed to.
  * Expose a few attribute docs to Sphinx.

0.1
  * Initial release. In production on support.mozilla.com. API may change.

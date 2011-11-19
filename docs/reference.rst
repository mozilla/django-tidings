=======================
Reference Documentation
=======================

After understanding the basic concepts of tidings from the :doc:`introduction`,
these docstrings make a nice comprehensive reference.

events
------

.. automodule:: tidings.events

  .. autoclass:: Event
    :members:
    :private-members:

  .. autoclass:: EventUnion
    :members:
    :private-members:

    .. automethod:: __init__

  .. autoclass:: InstanceEvent
    :members:
    :private-members:

    .. automethod:: __init__

  .. autoexception:: ActivationRequestFailed

models
------

.. automodule:: tidings.models
    :members:

tasks
-----

.. automodule:: tidings.tasks
    
    .. autofunction:: claim_watches(user)

utils
-----

.. automodule:: tidings.utils
    :members: hash_to_unsigned, emails_with_users_and_watches

views
-----

.. automodule:: tidings.views
    :members:
    :noindex:

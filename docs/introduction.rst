Introduction
============

Here we introduce django-tidings by way of examples and discuss some theory behind
its design.

A Simple Example
----------------

On support.mozilla.com, we host a wiki which houses documents in 80 different
human languages. For each document, we keep a record of revisions (in the
standard wiki fashion) stretching back to the document's creation::

  Document ---- Revision 1
            \__ Revision 2
            \__ Revision 3
            \__ ...

We let users register their interest in (or *watch*) a specific language, and
they are notified when any document in that language is edited. In our "edit
page" view, we explicitly let the system know that a noteworthy event has
occurred, like so...

::

  EditInLanguageEvent(revision).fire()

...which, if ``revision``'s document was written in English, sends a mail to
anyone who was watching English-language edits. The watching would have been
effected through view code like this::

  def watch_language(request):
      """Start notifying the current user of edits in the request's language."""
      EditInLanguageEvent.notify(request.user, language=request.locale)
      # ...and then render a page or something.

Thus we introduce the two core concepts of django-tidings:

  **Events**
    Things that occur, like the editing of a document in a certain language

  **Watches**
    Subscriptions. Specifically, mappings from events to the users or email
    addresses which are interested in them

Everything in tidings centers around these two types of objects.

Events, Watches, and Scoping
----------------------------

django-tidings is basically a big dispatch engine: something happens (that is,
an :class:`~tidings.events.Event` subclass fires), and tidings then has to
determine which  :class:`Watches <tidings.models.Watch>` are relevant so it knows
whom to mail. Each kind of event has an ``event_type``, an arbitrary string
that distinguishes it, and each watch references an event subclass by that
string. However, there is more to the watch-event relationship than that; a
watch has a number of other fields which can further refine its scope::

  watch ---- event_type
         \__ content_type
         \__ object_id
         \__ 0..n key/value pairs ("filters")

In addition to an event type, a watch may also reference a content type, an
object ID, and one or more *filters*, key/value pairs whose values come out of
an enumerated set (no larger than integer space). The key concept in
django-tidings, the one which gives it its flexibility, is that **only an Event
subclass determines the meaning of its Watches' fields**. ``event_type`` always
points to an Event subclass, but that is the only constant. ``content_type``
and ``object_id`` are almost always used as their names imply—but only by
convention. And filters are designed from the start to be arbitrary.

As a user of django-tidings, you will be writing a lot of Event subclasses and
deciding how to make use of Watch's fields for each. Let's take apart our
simple example to see how the ``EditInLanguageEvent`` class might be designed:

.. _edit-in-language-event:

.. code-block:: python
   :linenos:
   
    class EditInLanguageEvent(Event):
        """Event fired when any document in a certain language is edited
  
        Takes a revision when constructed and filters according to that
        revision's document's language
  
        notify(), stop_notifying(), and is_notifying() take these args:
  
            (user_or_email, language=some_language)
  
        """
        event_type = 'edited wiki document in language'
        filters = set(['language'])  # for validation only
    
        def __init__(self, revision):
            super(EditInLanguageEvent, self).__init__()
            self.revision = revision
    
        def _users_watching(self, **kwargs):
            return self._users_watching_by_filter(
                language=self.revision.document.language,
                **kwargs)
  
        ...

This event makes use of only two :class:`~tidings.models.Watch` fields: the
``event_type`` (which is implicitly handled by the framework) and a filter with
the key "language". ``content_type`` and ``object_id`` are unused. The action
happens in the ``_users_watching()`` method, which :meth:`Event.fire()
<tidings.events.Event.fire>` calls to determine whom to mail. Line 20 calls
:meth:`~tidings.events.Event._users_watching_by_filter`, which is the most
interesting method in the entire framework. In essence, this line says "Find me
all the watches matching my ``event_type`` and having a 'language' filter with
the value ``self.revision.document.language``." (It is always a good idea to
pass ``**kwargs`` along so you can support the :meth:`exclude
<tidings.events.Event._users_watching_by_filter>` option.)

Watch Filters
.............

This is a good point to say a word about :class:`WatchFilters
<tidings.models.WatchFilter>`. A filter is a key/value pair. The key is a
string and goes into the database verbatim. The value, however, is only a
4-byte unsigned int. If you pass a string as a watch filter value, it will be
hashed to make it fit. Thus, watch filters are no good for *storing* data but
only for distinguishing among members of enumerated sets.

An exception is if you pass an integer as a filter value. The framework will
notice this and let the int through unmodified. Thus, you can put (unchecked)
integer foreign key references into filters quite happily.

Details of the hashing behavior are documented in
:func:`~tidings.utils.hash_to_unsigned`.

Wildcards
.........

Think back to our :meth:`~tidings.events.Event.notify` call::

  EditInLanguageEvent.notify(request.user, language=request.locale)

It tells the framework to create a watch with the ``event_type`` ``'edited wiki
document in locale'`` (tying it to ``EditInLanguageEvent``) and a filter
mapping "language" to some locale.

Now, what if we had made this call instead, omitting the ``language`` kwarg?

::

  EditInLanguageEvent.notify(request.user)

This says "``request.user`` is interested in *every* ``EditInLanguageEvent``,
regardless of language", simply by omission of the "language" filter. A similar
logic applies to events which use the ``content_type`` or ``object_id`` fields:
leave them blank in a call to :meth:`~tidings.events.Event.notify`, and the
user will watch events with any value of them.

.. _uniquify:

If, for some odd reason, a user ends up watching both *all*
``EditInLanguageEvents`` and German ``EditInLanguageEvents`` in particular,
never fear: he will not receive two mails every time someone edits a German
article. tidings will automatically de-duplicate users within the scope of one
event class. Also, when faced with a registered user and an anonymous
subscription having the same email address, tidings will favor the registered
user. That way, any mails you generate will have the opportunity to use a nice
username, etc.

Completing the Event Implementation
-----------------------------------

A few more methods are necessary to get to a fully working
:ref:`EditInLanguageEvent <edit-in-language-event>`. Let's add them now:

.. code-block:: python
  
  class EditInLanguageEvent(Event):

      # Previous methods here
       
      def _mails(self, users_and_watches):
          """Construct the mails to send."""
          document = self.revision.document
  
          # This loop is shown for clarity, but in real code, you should use
          # the tidings.utils.emails_with_users_and_watches convenience
          # function.
          for user, watches in users_and_watches:
              yield EmailMessage(
                  'Notification: an edit!',
                  'Document %s was edited.' % document.title,
                  settings.TIDINGS_FROM_ADDRESS,
                  [user.email])

      @classmethod
      def _activation_email(cls, watch, email):
          """Return an EmailMessage to send to anonymous watchers.
      
          They are expected to follow the activation URL sent in the email to
          activate their watch, so you should include at least that.
      
          """
          return EmailMessage(
              'Confirm your subscription',
              'Click the link if you really want to subscribe: %s' % \
                  cls._activation_url(watch)
              settings.TIDINGS_FROM_ADDRESS,
              [email])

      @classmethod
      def _activation_url(cls, watch):
          """Return a URL pointing to a view that activates the watch."""
          return reverse('myapp.activate_watch', args=[watch.id, watch.secret])

Default implementations of :meth:`~tidings.events.Event._activation_email` and
:meth:`~tidings.events.Event._activation_url` are coming in a future version of
tidings.

Watching an Instance
--------------------

Often, we want to watch for changes to a specific object rather than a class of
them. tidings comes with a purpose-built abstract superclass for this,
:class:`~tidings.events.InstanceEvent`.

In the support.mozilla.com wiki, we allow a user to watch a specific document.
For example...

::

  EditDocumentEvent.notify(request.user, document)

With the help of :class:`~tidings.events.InstanceEvent`, this event can be
implemented just by choosing an ``event_type`` and a ``content_type`` and,
because we need Revision info in addition to Document info when we build the
mails, overriding ``__init__()``::

  class EditDocumentEvent(InstanceEvent):
      """Event fired when a certain document is edited"""
      event_type = 'wiki edit document'
      content_type = Document
  
      def __init__(self, revision):
          """This is another common pattern: we need to pass the Document to
          InstanceEvent's constructor, but we also need to keep the new
          Revision around so we can pull info from it when building our
          mails."""
          super(EditDocumentEvent, self).__init__(revision.document)
          self.revision = revision
  
      def _mails(self, users_and_watches):
          # ...

For more detail, see the :class:`~tidings.events.InstanceEvent` documentation.


De-duplication
--------------

We have already established that :ref:`mails get de-duplicated within the scope
of one event class <uniquify>`, but what about across many events? What happens
when a document is edited and some user was watching both it specifically and
its language in general? Does he receive two mails? Not if you use
:class:`~tidings.events.EventUnion`.

When your code does something that could cause both events to happen, the naive
approach would be to call them serially::

  EditDocumentEvent(revision).fire()
  EditInLanguageEvent(revision).fire()

That *would* send two mails. But if we use the magical
:class:`~tidings.events.EventUnion` construct instead...

::

  EventUnion(EditDocumentEvent(revision), EditInLanguageEvent(revision)).fire()

...tidings is informed that you're firing a bunch of events, and it sends only
one mail.

A few notes:

* The :meth:`~tidings.events.Event._mails` method from the first event class
  passed is the one that's used, though you can change this by subclassing
  :class:`~tidings.events.EventUnion` and overriding its
  :meth:`~tidings.events.EventUnion._mails`.
* Like the single-event de-duplication, :class:`~tidings.events.EventUnion`
  favors registered users over anonymous email addresses.

The Container Pattern
---------------------

One common case for de-duplication is when watchable objects contain other
watchable objects, as in a discussion forum where users can watch both threads
and entire forums::

  forum ---- thread
         \__ thread
         \__ thread

In this case, we might imagine having a ``NewPostInThreadEvent`` through which
users watch a thread and a ``NewPostInForumEvent`` through which they watch a
whole forum. Both events would be :class:`~tidings.events.InstanceEvent`
subclasses:

.. code-block:: python
  :linenos:
   
    class NewPostInForumEvent(InstanceEvent):
        event_type = 'new post in forum'
        content_type = Forum
    
        def __init__(self, post):
            super(NewPostInForumEvent, self).__init__(post.thread.forum)
            # Need to store the post for _mails
            self.post = post
  
  
    class NewPostInThreadEvent(InstanceEvent):
        event_type = 'new post in thread'
        content_type = Thread
    
        def __init__(self, post):
            super(NewPostInThreadEvent, self).__init__(post.thread)
            # Need to store the post for _mails
            self.post = post
    
        def fire(self, **kwargs):
            """Notify not only watchers of this thread but of the parent forum as well."""
            return EventUnion(self, NewPostInForumEvent(self.post)).fire(**kwargs)
    
        def _mails(self, users_and_watches):
            return emails_with_users_and_watches(
                'New post: %s' % self.post.title,
                'forums/email/new_post.ltxt',
                dict(post=post),
                users_and_watches)

On line 20, we cleverly override ``fire()``, replacing InstanceEvent's simple
implementation with one that fires the union of both events. Thus, callers need
only ever fire ``NewPostInThreadEvent``, and it will take care of the rest.

Since ``NewPostInForumEvent`` will now be fired only from an
:class:`~tidings.events.EventUnion` (and not as the first argument), it can get
away without a ``_mails`` implementation. The container pattern is very
slimming, both to callers and events.

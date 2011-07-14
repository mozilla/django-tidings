# -*- coding: utf-8 -*-
import mock
from nose.tools import eq_

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.mail import EmailMessage

from tidings.events import Event, _unique_by_email, EventUnion, InstanceEvent
from tidings.models import Watch, EmailUser
from tidings.tests import watch, watch_filter, ModelsTestCase, TestCase, user
from tidings.tests.models import MockModel


TYPE = 'some event'
ANOTHER_TYPE = 'another type'


class SimpleEvent(Event):
    event_type = TYPE

    def _mails(self, users_and_watches):
        """People watch the event in general; there are no parameters."""
        return (EmailMessage('Subject!', 'Body!', to=[u.email]) for u, w in
                users_and_watches)


class AnotherEvent(Event):
    event_type = ANOTHER_TYPE


class ContentTypeEvent(SimpleEvent):
    content_type = ContentType  # saves mocking a model


class FilteredEvent(SimpleEvent):
    filters = set(['color', 'flavor'])


class FilteredContentTypeEvent(ContentTypeEvent):
    filters = set(['color', 'flavor'])


class UsersWatchingTests(TestCase):
    """Unit tests for Event._users_watching_by_filter()"""

    @staticmethod
    def _emails_eq(addresses, event, **filters):
        """Assert that the given emails are the ones watching `event`, given
        the scoping in `filters`."""
        eq_(sorted(addresses),
            sorted([u.email for u, w in
                    event._users_watching_by_filter(**filters)]))

    def test_simple(self):
        """Test whether a watch scoped only by event type fires for both
        anonymous and registered users."""
        registered_user = user(email='regist@ered.com', save=True)
        watch(event_type=TYPE, user=registered_user).save()
        watch(event_type=TYPE, email='anon@ymous.com').save()
        watch(event_type='something else', email='never@fires.com').save()
        self._emails_eq(['regist@ered.com', 'anon@ymous.com'], SimpleEvent())

    def test_inactive(self):
        """Make sure inactive watches don't fire."""
        watch(event_type=TYPE, email='anon@ymous.com', is_active=False).save()
        watch(event_type=TYPE, email='active@one.com').save()
        self._emails_eq(['active@one.com'], SimpleEvent())

    def test_content_type(self):
        """Make sure watches filter properly by content type."""
        watch_type = ContentType.objects.get_for_model(Watch)
        content_type_type = ContentType.objects.get_for_model(ContentType)
        registered_user = user(email='regist@ered.com', save=True)
        watch(event_type=TYPE, content_type=content_type_type,
              user=registered_user).save()
        watch(event_type=TYPE, content_type=content_type_type,
              email='anon@ymous.com').save()
        watch(event_type=TYPE, content_type=watch_type,
              email='never@fires.com').save()
        self._emails_eq(['regist@ered.com', 'anon@ymous.com'],
                        ContentTypeEvent())

    def test_filtered(self):
        """Make sure watches cull properly by additional filters."""
        # A watch with just the filter we're searching for:
        registered_user = user(email='ex@act.com', save=True)
        exact_watch = watch(event_type=TYPE, user=registered_user, save=True)
        watch_filter(watch=exact_watch, name='color', value=1).save()

        # A watch with extra filters:
        extra_watch = watch(event_type=TYPE, email='extra@one.com', save=True)
        watch_filter(watch=extra_watch, name='color', value=1).save()
        watch_filter(watch=extra_watch, name='flavor', value=2).save()

        # A watch with no row for the filter we're searching on:
        watch(event_type=TYPE, email='wild@card.com').save()

        # A watch with a mismatching filter--shouldn't be found
        mismatch_watch = watch(event_type=TYPE, email='mis@match.com',
                               save=True)
        watch_filter(watch=mismatch_watch, name='color', value=3).save()

        self._emails_eq(['ex@act.com', 'extra@one.com', 'wild@card.com'],
                        FilteredEvent(), color=1)

        # Search on multiple filters to test joining the filters table twice.
        # We provide values that match for both filters, as mis@match.com
        # suffices to test exclusion.
        self._emails_eq(['ex@act.com', 'extra@one.com', 'wild@card.com'],
                        FilteredEvent(), color=1, flavor=2)

    def test_bad_filters(self):
        """Bad filter types passed in should throw TypeError."""
        self.assertRaises(TypeError, SimpleEvent()._users_watching_by_filter,
                          smoo=3)

    def test_duplicates(self):
        """Don't return duplicate email addresses."""
        watch(event_type=TYPE, user=user(email='hi@there.com', save=True),
              save=True)
        watch(event_type=TYPE, email='hi@there.com').save()
        watch(event_type=TYPE, email='hi@there.com').save()
        eq_(3, Watch.objects.all().count())  # We created what we meant to.

        self._emails_eq(['hi@there.com'], SimpleEvent())

    def test_duplicates_case_insensitive(self):
        """De-duping should compare case-insensitively."""
        watch(event_type=TYPE, user=user(email='HI@example.com', save=True),
              save=True)
        watch(event_type=TYPE, email='hi@EXAMPLE.com').save()
        watch(event_type=TYPE, email='hi@EXAMPLE.com').save()
        eq_(3, Watch.objects.all().count())  # We created what we meant to.

        addresses = [u.email
                     for u, w in SimpleEvent()._users_watching_by_filter()]
        eq_(1, len(addresses))
        eq_('hi@example.com', addresses[0].lower())

    def test_registered_users_favored(self):
        """When removing duplicates, make sure registered users are kept in
        favor of anonymous ones having the same email address."""
        def make_anonymous_watches():
            for x in xrange(3):
                watch(event_type=TYPE, email='hi@there.com').save()

        # Throw some anonymous watches in there in the hope that they would
        # come out on top if we didn't purposely favor registered users.
        # Suggestions on how to make this test more reliable are welcome.
        make_anonymous_watches()

        # File the registered watch:
        watch(event_type=TYPE,
              user=user(first_name='Jed', email='hi@there.com',
                        save=True)).save()

        # A few more anonymous watches in case the BTrees flop in the other
        # direction:
        make_anonymous_watches()

        users_and_watches = list(SimpleEvent()._users_watching_by_filter())
        u, w = users_and_watches[0]
        eq_('Jed', u.first_name)

    def test_unique_by_email_user_selection(self):
        """Test the routine that sorts through users and watches having the
        same email addresses."""
        # Test the best in a cluster coming first, in the middle, and last.
        # We mark the correct choices with first_name='a'.
        users_and_watches = [
            (user(first_name='a', email='hi'), [watch()]),
            (user(email='hi'), [watch()]),
            (user(), [watch(email='hi')]),

            (user(), [watch(email='mid')]),
            (user(first_name='a', email='mid'), [watch()]),
            (user(), [watch(email='mid')]),

            (user(), [watch(email='lo')]),
            (user(), [watch(email='lo')]),
            (user(first_name='a', email='lo'), [watch()]),

            (user(), [watch(email='none', secret='a')]),
            (user(), [watch(email='none')])]

        favorites = list(_unique_by_email(users_and_watches))
        eq_(4, len(favorites))

        # Test that we chose the correct users, where there are distinguishable
        # (registered) users to choose from:
        eq_(['a'] * 3, [u.first_name for u, w in favorites[:3]])

    def test_unique_by_email_watch_collection(self):
        """Make sure _unique_by_email() collects all watches in each cluster."""
        w1, w2, w3 = watch(), watch(), watch(email='hi')
        w4, w5, w6 = watch(), watch(), watch(email='lo')
        users_and_watches = [
            (user(email='hi'), [w1]),
            (user(email='hi'), [w2]),
            (user(), [w3]),

            (user(email='lo'), [w4]),
            (user(email='lo'), [w5]),
            (user(), [w6])]
        result = list(_unique_by_email(users_and_watches))

        _, watches = result[0]
        eq_(set([w1, w2, w3]), set(watches))

        # Make sure the watches accumulator gets cleared between clusters:
        _, watches = result[1]
        eq_(set([w4, w5, w6]), set(watches))

    def test_unsaved_exclude(self):
        """Excluding an unsaved user should throw a ValueError."""
        self.assertRaises(ValueError,
                          SimpleEvent()._users_watching_by_filter,
                          exclude=user())


class EventUnionTests(TestCase):
    """Tests for EventUnion"""

    @staticmethod
    def _emails_eq(addresses, event):
        """Assert that the given emails are the ones watching `event`."""
        eq_(sorted(addresses),
            sorted([u.email for u, w in
                    event._users_watching()]))

    def test_merging(self):
        """Test that duplicate emails across multiple events get merged."""
        watch(event_type=TYPE, email='he@llo.com').save()
        watch(event_type=TYPE, email='ick@abod.com').save()
        registered_user = user(email='he@llo.com', save=True)
        watch(event_type=ANOTHER_TYPE, user=registered_user).save()

        self._emails_eq(['he@llo.com', 'ick@abod.com'],
                        EventUnion(SimpleEvent(), AnotherEvent()))

    def test_duplicates_case_insensitive(self):
        """Test that duplicate merging is case insensitive."""
        # These mocks return their users in descending order like the SQL
        # query.
        class OneEvent(object):
            def _users_watching(self):
                return [(user(email='HE@LLO.COM'), [watch()])]

        class AnotherEvent(object):
            def _users_watching(self):
                return [(user(email='he@llo.com'), [watch()]),
                        (user(email='br@illo.com'), [watch()])]

        addresses = [u.email for u, w in
                     EventUnion(OneEvent(),
                                AnotherEvent())._users_watching()]

        eq_(2, len(addresses))
        eq_('he@llo.com', addresses[0].lower())

    @mock.patch.object(SimpleEvent, '_mails')
    def test_fire(self, _mails):
        """Assert firing the union gets the mails from the first event."""
        _mails.return_value = []
        watch(event_type=TYPE, email='he@llo.com').save()
        EventUnion(SimpleEvent(), AnotherEvent()).fire()
        assert _mails.called

    def test_watch_lists(self):
        """Ensure the Union returns every watch a user has."""
        w1 = watch(event_type=TYPE, email='jeff@here.com', save=True)
        w2 = watch(event_type=TYPE, email='jeff@here.com', save=True)
        u, w = list(EventUnion(SimpleEvent())._users_watching())[0]
        eq_([w1, w2], sorted(w, key=lambda x: x.id))


class NotificationTests(TestCase):
    """Tests for Event methods that create, examine, and destroy watches."""

    def test_lifecycle(self):
        """Vet the creation, testing, and deletion of watches.

        Test registered users and anonymous email addresses. Test content_types
        and general filters.

        """
        EMAIL = 'fred@example.com'
        FilteredContentTypeEvent.notify(EMAIL, color=1)
        assert FilteredContentTypeEvent.is_notifying(EMAIL, color=1)

        FilteredContentTypeEvent.stop_notifying(EMAIL, color=1)
        assert not FilteredContentTypeEvent.is_notifying(EMAIL, color=1)

    def test_notify_idempotence(self):
        """Assure notify() returns an existing watch when possible."""
        u = user(save=True)
        w = FilteredContentTypeEvent.notify(u, color=3, flavor=4)
        eq_(w.pk, FilteredContentTypeEvent.notify(u, color=3, flavor=4).pk)
        eq_(1, Watch.objects.all().count())

    def test_duplicate_tolerance(self):
        """Assure notify() returns an existing watch if there is a matching
        one.

        Also make sure it returns only 1 watch even if there are duplicate
        matches.

        """
        w1 = watch(event_type=TYPE, email='hi@there.com', save=True)
        w2 = watch(event_type=TYPE, email='hi@there.com', save=True)
        assert SimpleEvent.notify('hi@there.com').pk in [w1.pk, w2.pk]

    def test_exact_matching(self):
        """Assert is_notifying() doesn't match watches having a superset of
        the given filters."""
        FilteredContentTypeEvent.notify('hi@there.com', color=3, flavor=4)
        assert not FilteredContentTypeEvent.is_notifying('hi@there.com',
                                                         color=3)

    def test_anonymous(self):
        """Anonymous users with no emails can't be watching anything.

        Mostly, this is just to make sure it doesn't crash.

        """
        assert not SimpleEvent.is_notifying(AnonymousUser())

    def test_hashing(self):
        """Strings should be hashed to ints, but ints should be left alone.

        Unicode strings should also work.

        """
        FilteredEvent.notify('red@x.com', color='red', flavor=6)
        FilteredEvent.notify('blue@x.com', color=u'blüe', flavor=7)
        assert FilteredEvent.is_notifying('red@x.com', color='red', flavor=6)
        assert FilteredEvent.is_notifying('blue@x.com', color=u'blüe',
                                          flavor=7)
        assert not FilteredEvent.is_notifying('blue@x.com', color='red',
                                              flavor=7)


class CascadingDeleteTests(ModelsTestCase):
    """Cascading deletes on object_id + content_type."""
    apps = ['tidings.tests']

    def test_mock_model(self):
        """Deleting an instance of MockModel should delete watches.

        Create instance of MockModel from tidings.tests.models, then
        delete it and watch the cascade go.

        """
        mock_m = MockModel.objects.create()
        watch(event_type=TYPE, email='hi@there.com', content_object=mock_m,
              save=True)
        MockModel.objects.all().delete()
        assert not Watch.objects.count(), 'Cascade delete failed.'


class MailTests(TestCase):
    """Tests for mail-sending and templating"""

    @mock.patch.object(settings._wrapped, 'TIDINGS_CONFIRM_ANONYMOUS_WATCHES', False)
    def test_fire(self):
        """Assert that fire() runs and that generated mails get sent."""
        SimpleEvent.notify('hi@there.com').activate().save()
        SimpleEvent().fire()

        eq_(1, len(mail.outbox))
        first_mail = mail.outbox[0]
        eq_(['hi@there.com'], first_mail.to)
        eq_('Subject!', first_mail.subject)
        eq_('Body!', first_mail.body)

    def test_anonymous_notify_and_fire(self):
        """Calling notify() sends confirmation email, and calling fire() sends
        notification email."""
        w = SimpleEvent.notify('hi@there.com')

        eq_(1, len(mail.outbox))
        first_mail = mail.outbox[0]
        eq_(['hi@there.com'], first_mail.to)
        eq_('TODO', first_mail.subject)
        eq_('Activate!', first_mail.body)

        w.activate().save()
        SimpleEvent().fire()

        second_mail = mail.outbox[1]
        eq_(['hi@there.com'], second_mail.to)
        eq_('Subject!', second_mail.subject)
        eq_('Body!', second_mail.body)

    @mock.patch.object(settings._wrapped, 'TIDINGS_CONFIRM_ANONYMOUS_WATCHES', False)
    def test_exclude(self):
        """Assert the `exclude` arg to fire() excludes the given user."""
        SimpleEvent.notify('du@de.com').activate().save()
        registered_user = user(email='ex@clude.com', save=True)
        SimpleEvent.notify(registered_user).activate().save()

        SimpleEvent().fire(exclude=registered_user)

        eq_(1, len(mail.outbox))
        first_mail = mail.outbox[0]
        eq_(['du@de.com'], first_mail.to)
        eq_('Subject!', first_mail.subject)

    @mock.patch.object(settings._wrapped, 'TIDINGS_CONFIRM_ANONYMOUS_WATCHES', False)
    def test_exclude_multiple(self):
        """Show that passing a sequence to exclude excludes them all."""
        SimpleEvent.notify('du@de.com').activate().save()
        user1 = user(email='ex1@clude.com', save=True)
        SimpleEvent.notify(user1).activate().save()
        user2 = user(email='ex2@clude.com', save=True)
        SimpleEvent.notify(user2).activate().save()

        SimpleEvent().fire(exclude=[user1, user2])

        eq_(1, len(mail.outbox))
        eq_(['du@de.com'], mail.outbox[0].to)


def test_anonymous_user_compares():
    """Make sure anonymous users with different emails compare different."""
    # Test __ne__:
    assert EmailUser('frank') != EmailUser('george')
    assert not EmailUser('frank') != EmailUser('frank')

    # Test __eq__:
    assert not EmailUser('frank') == EmailUser('george')
    assert EmailUser('frank') == EmailUser('frank')

    # Test __hash__:
    assert hash(EmailUser('frank')) == hash(EmailUser('frank'))
    assert hash(EmailUser('frank')) != hash(EmailUser('george'))


class MockModelEvent(InstanceEvent):
    event_type = 'mock model event'
    content_type = MockModel


class InstanceEventTests(ModelsTestCase):
    apps = ['tidings.tests']

    def _test_user_or_email(self, user_or_email):
        """Test all states of the truth table for 2 instances being watched.

        E.g. watch m, assert watching m but not m2; watch m2, assert watching
        both, etc.

        """
        mock_m = MockModel.objects.create()
        mock_m2 = MockModel.objects.create()
        MockModelEvent.notify(user_or_email, mock_m)
        # We're watching instance #1...
        assert MockModelEvent.is_notifying(user_or_email, mock_m)
        # ... but not instance #2
        assert not MockModelEvent.is_notifying(user_or_email, mock_m2)
        # Now also watch instance #2.
        MockModelEvent.notify(user_or_email, mock_m2)
        assert MockModelEvent.is_notifying(user_or_email, mock_m)
        assert MockModelEvent.is_notifying(user_or_email, mock_m2)
        # Stop watching instance #1...
        MockModelEvent.stop_notifying(user_or_email, mock_m)
        assert not MockModelEvent.is_notifying(user_or_email, mock_m)
        assert MockModelEvent.is_notifying(user_or_email, mock_m2)
        # ... and instance #2
        MockModelEvent.stop_notifying(user_or_email, mock_m2)
        assert not MockModelEvent.is_notifying(user_or_email, mock_m2)
        # No watch objects are left over.
        assert not Watch.objects.count()

    def test_instance_anonymous(self):
        """Watch with an anonymous user."""
        self._test_user_or_email('fred@example.com')

    def test_instance_registered(self):
        """Watch with a registered user."""
        registered_user = user(email='regist@ered.com', save=True)
        self._test_user_or_email(registered_user)

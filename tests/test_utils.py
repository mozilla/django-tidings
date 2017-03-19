from django.core.exceptions import ImproperlyConfigured
from django.utils.six.moves import range, reduce

from tidings.utils import collate, import_from_setting

from .base import TestCase, override_settings


class MergeTests(TestCase):
    """Unit tests for collate()"""

    def test_default(self):
        """Test with the default `key` function."""
        iterables = [range(4), range(7), range(3, 6)]
        self.assertEqual(sorted(reduce(list.__add__,
                                       [list(it) for it in iterables])),
                         list(collate(*iterables)))

    def test_key(self):
        """Test using a custom `key` function."""
        iterables = [range(5, 0, -1), range(4, 0, -1)]
        self.assertEqual(list(sorted(reduce(list.__add__,
                                            [list(it) for it in iterables]),
                                     reverse=True)),
                         list(collate(*iterables, key=lambda x: -x)))

    def test_empty(self):
        """Be nice if passed an empty list of iterables."""
        self.assertEqual([], list(collate()))

    def test_one(self):
        """Work when only 1 iterable is passed."""
        self.assertEqual([0, 1], list(collate(range(2))))

    def test_reverse(self):
        """Test the `reverse` kwarg."""
        iterables = [range(4, 0, -1), range(7, 0, -1), range(3, 6, -1)]
        self.assertEqual(sorted(reduce(list.__add__,
                                       [list(it) for it in iterables]),
                                reverse=True),
                         list(collate(*iterables, reverse=True)))


class ImportedFromSettingTests(TestCase):
    """Tests for import_from_setting() and _imported_symbol()"""

    @override_settings(TIDINGS_MODEL_BASE='django.db.models.Model')
    def test_success(self):
        from django.db.models import Model
        assert import_from_setting('TIDINGS_MODEL_BASE', 'blah') == Model

    @override_settings(
            TIDINGS_MODEL_BASE='hummahummanookanookanonexistent.thing')
    def test_module_missing(self):
        self.assertRaises(ImproperlyConfigured,
                          import_from_setting, 'TIDINGS_MODEL_BASE', 'blah')

    @override_settings(TIDINGS_MODEL_BASE='hummahummanookanookanonexistent')
    def test_symbol_missing(self):
        self.assertRaises(ImproperlyConfigured,
                          import_from_setting, 'TIDINGS_MODEL_BASE', 'blah')

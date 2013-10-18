import djcelery
import os

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

# Django
DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'djcelery',
    'tidings',
    'south',
    'test_app',
]
ROOT_URLCONF = 'test_app.urls'
SITE_ID = 1
TEMPLATE_DEBUG = True
TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

# Jinja
TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path('templates')
]
TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)
JINGO_INCLUDE_PATTERN = r'\.html'

# Celery
djcelery.setup_loader()
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True  # Explode loudly during tests.

# Tidings
TIDINGS_FROM_ADDRESS = 'nobody@example.com'
TIDINGS_CONFIRM_ANONYMOUS_WATCHES = True

SECRET_KEY = 'yada-yada'

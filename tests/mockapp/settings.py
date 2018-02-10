'''Settings for test application.'''

# Django
DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'tidings',
    'tests',
    'tests.mockapp',
]
ROOT_URLCONF = 'tests.urls'
SECRET_KEY = 'yada-yada'
SITE_ID = 1
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
]

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True  # Explode loudly during tests.

# Tidings
TIDINGS_FROM_ADDRESS = 'nobody@example.com'
TIDINGS_CONFIRM_ANONYMOUS_WATCHES = True

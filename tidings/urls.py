from django.conf.urls import url

from .views import unsubscribe


urlpatterns = (
    url(r'^unsubscribe/(?P<watch_id>\d+)$',
        unsubscribe,
        name='tidings.unsubscribe'),
)

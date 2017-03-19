from django.conf.urls import include, patterns


urlpatterns = patterns(
    '',
    (r'^', include('tidings.urls'))
)

from django.conf.urls.defaults import include, patterns


urlpatterns = patterns('',
    (r'^', include('tidings.urls')))


handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

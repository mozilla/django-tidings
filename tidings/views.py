from django.conf import settings
from django.shortcuts import render

from tidings.models import Watch


def unsubscribe(request, watch_id):
    """Unsubscribe from (i.e. delete) the watch of ID ``watch_id``.

    Expects an ``s`` querystring parameter matching the watch's secret.

    GET will result in a confirmation page (or a failure page if the secret is
    wrong). POST will actually delete the watch (again, if the secret is
    correct).

    Uses these templates:

    * tidings/unsubscribe.html - Asks user to confirm deleting a watch
    * tidings/unsubscribe_error.html - Shown when a watch is not found
    * tidings/unsubscribe_success.html - Shown when a watch is deleted

    The shipped templates assume a ``head_title`` and a ``content`` block
    in a ``base.html`` template.

    The template extension can be changed from the default ``html`` using
    the setting :data:`~django.conf.settings.TIDINGS_TEMPLATE_EXTENSION`.
    """
    ext = getattr(settings, 'TIDINGS_TEMPLATE_EXTENSION', 'html')

    # Grab the watch and secret; complain if either is wrong:
    try:
        watch = Watch.objects.get(pk=watch_id)
        # 's' is for 'secret' but saves wrapping in mails
        secret = request.GET.get('s')
        if secret != watch.secret:
            raise Watch.DoesNotExist
    except Watch.DoesNotExist:
        return render(request, 'tidings/unsubscribe_error.' + ext)

    if request.method == 'POST':
        watch.delete()
        return render(request, 'tidings/unsubscribe_success.' + ext)

    return render(request, 'tidings/unsubscribe.' + ext)

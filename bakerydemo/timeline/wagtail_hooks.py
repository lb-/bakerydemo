from django.conf.urls import url
from django.http import HttpResponse
from django.urls import reverse

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from wagtail.core import hooks


def admin_view(request):
    return HttpResponse(
        "Timeline",
        content_type="text/plain")


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^timeline/$', admin_view, name='timeline'),
    ]


@hooks.register('register_admin_menu_item')
def register_timeline_menu_item():
    return MenuItem(
        'Timeline',
        reverse('timeline'),
        classnames='icon icon-folder-inverse',
        order=10000
    )

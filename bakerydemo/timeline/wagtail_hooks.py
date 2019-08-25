from django.conf.urls import url
from django.urls import reverse

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from .views import timeline_view


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^timeline/$', timeline_view, name='timeline'),
    ]


@hooks.register('register_admin_menu_item')
def register_timeline_menu_item():
    return MenuItem(
        'Timeline',
        reverse('timeline'),
        classnames='icon icon-time',
        order=10000
    )

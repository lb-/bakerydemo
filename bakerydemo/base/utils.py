from django.urls import path, reverse

from wagtail.admin.action_menu import ActionMenuItem
from wagtail.core import hooks

from .views import ArchiveView


class ArchiveMenuItem(ActionMenuItem):
    icon_name = "placeholder"
    name = "action-archive"
    label = "Archive"

    def get_url(self, context):
        # note: pre Wagtail 2.15, should be get_url(self, request, context)
        return reverse("archive", args=(context["page"].pk,))


def get_page_action_menu(menu_items, request, context):
    page = context["page"]
    can_archive = getattr(page, "can_archive", False)
    if can_archive:
        menu_items.insert(1, ArchiveMenuItem())
    return menu_items


def register_archive_hooks():
    hooks.register("construct_page_action_menu", get_page_action_menu)

    @hooks.register("register_admin_urls")
    def urlconf_time():
        # question: how do I get this to be 'archive:confirm'
        return [
            path(
                "archive/<str:pk>/confirm/",
                ArchiveView.as_view(),
                name="archive",
            ),
        ]

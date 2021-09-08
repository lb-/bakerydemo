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


def archive_log_actions(actions):
    actions.register_action("archive", "Archive", "Archived")


def get_urls():
    return [
        path(
            "archive/<str:pk>/confirm/",
            ArchiveView.as_view(),
            name="archive",
        ),
    ]


def register_archive_hooks():

    hooks.register("construct_page_action_menu", get_page_action_menu)
    hooks.register("register_admin_urls", get_urls)
    hooks.register("register_log_actions", archive_log_actions)

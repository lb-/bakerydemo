from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail.admin.viewsets.base import ViewSet

from wagtail import hooks



class ExplainViewSet(ViewSet):
    icon = "help"
    menu_label = "Explain"
    name = "explain"
    url_namespace = "explain"
    template_name = "base/explain.html"

    def index(self, request):
        return render(
            request,
            self.template_name,
            {"page_title": "Greetings", "header_icon": self.icon},
        )

    def get_urlpatterns(self):
        return [
            path("", self.index, name="index"),
        ]

@hooks.register("register_admin_viewset")
def register_viewset():
    return ExplainViewSet()

# @hooks.register('construct_help_menu')
# def add_explain_items(request, menu_items):
#   print(menu_items)

@hooks.register('register_help_menu_item')
def register_explain_menu_item():
  return MenuItem('Explain', reverse('explain:index'), icon_name='folder-inverse', order=10000)


# @hooks.register('register_admin_urls')
# def urlconf_time():
#   return [
#     path('how_did_you_almost_know_my_name/', admin_view, name='frank'),
#   ]



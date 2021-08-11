from django.http import HttpResponse
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.urls import path, reverse, resolve
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from wagtail.core import hooks
from wagtail.admin.menu import SubmenuMenuItem

from wagtail.contrib.modeladmin.menus import GroupMenuItem, SubMenu
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .models import HelpArticle

"""
* need to fix it so that the menu item can be viewed by all
* what if this was called Guide not Help?
* what if there was also a HelpSettings (in the settings item though)
* this would allow for showing tips for first time users
* also a welcome panel on the home page
* Inspect view could be prettier
* Idea is that admins would probably only edit, while all other users would just have view access
* would be epic if you did not have to actually go to the inspect page (just opens up a modal)
* do not try to be too smart with the URl mapping thing, just put a URL path admin/ & check with starts with??

Nice to have
* Would be great to be able to create entries automatically populated from Wagtail docs (even just as a one time)
* url_name should be unique (no dupes) but that is a nice to have, same with pre-filling
* import/export
* versioning
* viewing all in one page
* what if you could use chardin.js or intro.js & add a bunch of element selectors

"""

class HelpArticleAdmin(ModelAdmin):
    model = HelpArticle
    menu_icon = 'doc-full'
    menu_order = 100
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

    inspect_view_enabled = True


class HelpGroupMenuItem(GroupMenuItem):
    template = 'menu_help_group_item.html'

    def get_context(self, request):
        context = super().get_context(request)
        url_name = resolve(request.path_info).url_name
        # many admin pages just say 'index' (e.g. forms index)
        # and page edit, image edit both have 'edit'
        # might need to think of a tag system so you add multiple tags
        # images, edit -> pulls the URL parts out and the url name to attempt to build something
        context['current_url_name'] = url_name
        help_article = HelpArticle.objects.filter(url_name=url_name).first()

        if help_article:
            context['help_article'] = help_article
            help_article_url = reverse(HelpArticleAdmin().url_helper.get_action_url_name('inspect'), kwargs={'instance_pk': help_article.pk})
            context['help_article_url'] = help_article_url
            context['classnames'] = context['classnames'] + ' help-available'
            print('menu context!', help_article_url)

        return context


class HelpGroup(ModelAdminGroup):
    menu_label = 'Help'
    menu_icon = 'help'
    menu_order = 10000
    items = (HelpArticleAdmin,)


    def get_menu_item(self):
        """
        Utilised by Wagtail's 'register_menu_item' hook to create a menu
        for this group with a SubMenu linking to listing pages for any
        associated ModelAdmin instances
        """
        if self.modeladmin_instances:
            submenu = SubMenu(self.get_submenu_items())
            return HelpGroupMenuItem(self, self.get_menu_order(), submenu)

class TourPanel:
    order = 50

    def __init__(self, request):
        self.request = request

    def render(self):
        if self.request.user.is_superuser:
            return ""
        else:
            return render_to_string('help_homepage_panel.html', {}, request=self.request)



@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(TourPanel(request))

# cannot use this as it will put css after but we want to use wagtail styles as priority
# @hooks.register('insert_global_admin_css')
# def global_admin_css():
#     return format_html('<link rel="stylesheet" href="{}">', 'https://cdn.jsdelivr.net/npm/shepherd.js@8/dist/css/shepherd.css')

@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html('<script src="{}"></script>','https://cdn.jsdelivr.net/npm/shepherd.js@8/dist/js/shepherd.min.js')


modeladmin_register(HelpGroup)

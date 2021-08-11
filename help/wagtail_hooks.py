from django.http import HttpResponse
from django.urls import path, reverse, resolve

from wagtail.core import hooks
from wagtail.admin.menu import SubmenuMenuItem

from wagtail.contrib.modeladmin.menus import GroupMenuItem, SubMenu
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .models import HelpArticle


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
        context['current_url_name'] = url_name
        help_article = HelpArticle.objects.filter(url_name=url_name).first()

        if help_article:
            context['help_article'] = help_article
            # print('model_admin', self.model_admin)
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


modeladmin_register(HelpGroup)

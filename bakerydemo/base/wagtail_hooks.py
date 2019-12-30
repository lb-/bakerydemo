from wagtail.admin.menu import MenuItem

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from bakerydemo.blog.models import BlogPage

class ModelAdminQueryMenuItem(MenuItem):

    def __init__(self, model_admin, order, query, label_append=''):
        self.model_admin = model_admin
        url = model_admin.url_helper.index_url + "?" + query
        classnames = 'icon icon-%s' % model_admin.get_menu_icon()
        super().__init__(
            label=model_admin.get_menu_label() + label_append,
            url=url,
            classnames=classnames,
            order=order
        )

    def is_shown(self, request):
        return self.model_admin.permission_helper.user_can_list(request.user)


class BlogPageAdmin(ModelAdmin):
    model = BlogPage

    def get_menu_items(self, order=None):
        # new class method that builds a list of menu_item(s)
        menu_items = []

        ## build 'live only' (no unpublished changes) items
        live_menu_item = ModelAdminQueryMenuItem(self, order or self.get_menu_order(), query='has_unpublished_changes=False', label_append=' (Live)')
        menu_items.append(live_menu_item)

        ## build 'draft' items
        draft_menu_item = ModelAdminQueryMenuItem(self, order or self.get_menu_order(), query='has_unpublished_changes=True', label_append=' (Draft)')
        menu_items.append(draft_menu_item)

        return menu_items

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        ## read the request and modify the qs as needed if query param does not work easily
        return qs

class BlogGroup(ModelAdminGroup):
    menu_label = 'Blog'
    items = (BlogPageAdmin, )

    def get_submenu_items(self):
        menu_items = []
        item_order = 1
        for modeladmin in self.modeladmin_instances:
            menu_items = menu_items + modeladmin.get_menu_items(item_order)
            item_order = len(menu_items) + 1
        return menu_items

modeladmin_register(BlogGroup)

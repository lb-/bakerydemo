from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .menu import GuideAdminMenuItem
from .models import Guide


class GuideAdmin(ModelAdmin):
    menu_label = "Guide"
    model = Guide
    menu_icon = "help"
    menu_order = 8000
    list_display = ("title", "url_path")
    search_fields = ("title", "url_path")
    inspect_view_enabled = True

    def get_menu_item(self, order=None):
        """
        Utilised by Wagtail's 'register_menu_item' hook to create a menu item
        to access the listing view, or can be called by ModelAdminGroup
        to create a SubMenu
        """
        return GuideAdminMenuItem(self, order or self.get_menu_order())


@hooks.register("insert_global_admin_js")
def global_admin_js():
    """
    Sourced from https://www.jsdelivr.com/package/npm/shepherd.js
    """
    return format_html(
        '<script src="{}"></script><script src="{}"></script>',
        "https://cdn.jsdelivr.net/npm/shepherd.js@8/dist/js/shepherd.min.js",
        static("js/shepherd.js"),
    )


@hooks.register("insert_global_admin_css")
def global_admin_css():
    """
    Pulled from https://github.com/shipshapecode/shepherd/releases (assets)
    .button styles removed (so we can use Wagtail styles instead)
    """
    return format_html('<link rel="stylesheet" href="{}">', static("css/shepherd.css"))


modeladmin_register(GuideAdmin)

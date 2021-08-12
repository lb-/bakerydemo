from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Guide


class GuideAdmin(ModelAdmin):
    menu_label = "Guide"
    model = Guide
    menu_icon = "help"
    menu_order = 8000
    list_display = ("title", "url_path")
    search_fields = ("title", "url_path")
    inspect_view_enabled = True


modeladmin_register(GuideAdmin)

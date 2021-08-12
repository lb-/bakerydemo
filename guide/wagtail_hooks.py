from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import Guide

class GuideAdmin(ModelAdmin):
    menu_label = 'Help'
    model = Guide
    menu_icon = 'help'
    menu_order = 8000
    list_display = ('title', 'url_path')
    search_fields = ('title', 'url_path')
    inspect_view_enabled = True


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        'https://cdn.jsdelivr.net/npm/shepherd.js@8/dist/js/shepherd.min.js'
    )


modeladmin_register(GuideAdmin)

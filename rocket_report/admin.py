from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import RocketReport


class RocketReportAdmin(ModelAdmin):
    model = RocketReport
    menu_icon = "fa-rocket"
    list_display = ("title", "status", "category", "submitted_by")
    list_filter = ("status", "category")
    search_fields = ("title", "status", "category", "submitted_by")

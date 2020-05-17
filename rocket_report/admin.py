from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import RocketReport


class KanbanMixin:
    def get_index_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return self.index_template_name or self.get_templates("kanban_index")


class RocketReportAdmin(KanbanMixin, ModelAdmin):
    model = RocketReport
    menu_icon = "fa-rocket"
    list_display = ("title", "status", "category", "submitted_by")
    list_filter = ("status", "category")
    search_fields = ("title", "status", "category", "submitted_by")

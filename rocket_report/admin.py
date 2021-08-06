from wagtail.contrib.modeladmin.options import ModelAdmin

from .views import KanbanView
from .models import RocketReport


class KanbanMixin:
    index_view_class = KanbanView

    def get_index_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return self.index_template_name or self.get_templates("kanban_index")


    def get_kanban_item_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return getattr(
            self, "kanban_item_template_name", self.get_templates("kanban_item")
        )

    def get_kanban_column_title_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return getattr(
            self,
            "kanban_column_title_template_name",
            self.get_templates("kanban_column_title"),
        )

    def get_kanban_column_field(self):
        # return a field to use to determine which column the item will be shown in
        # pull in the first value from list_filter if no specific column set
        list_filter = getattr(self, "list_filter", [])
        field = list_filter[0] if list_filter else None
        return field

    def get_kanban_column_name_default(self):
        # used for the column title name for None or no column scenarios
        return getattr(self, "kanban_column_name_default", "Other")


class RocketReportAdmin(KanbanMixin, ModelAdmin):
    model = RocketReport
    menu_icon = "fa-rocket"
    list_display = ("title", "status", "category", "submitted_by")
    list_filter = ("status", "category")
    search_fields = ("title", "status", "category", "submitted_by")

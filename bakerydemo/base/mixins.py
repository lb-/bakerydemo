from .views import KanbanView


class KanbanMixin:
    index_view_class = KanbanView

    def get_index_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return self.index_template_name or self.get_templates("kanban")

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
        # pull in the first value from list_filder if no specific column set
        list_filter = getattr(self, "list_filter", [])
        field = list_filter[0] if list_filter else None
        return field

    def get_kanban_column_name_default(self):
        # used for the column title name for None or no column scenarios
        return getattr(self, "kanban_column_name_default", "Other")

    def get_kanban_column_change_handler(self):
        # see if a change handler is set and return it or None if not supplied
        # used to dertmine if drag/drop is available on this board
        return getattr(self, "handle_kanban_column_change", None,)

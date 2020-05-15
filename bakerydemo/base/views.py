from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):
    def get_context_data(self, **kwargs):
        kanban_element_id = "kanban"
        kanban_options = {
            "addItemButton": True,
            "boards": [
                {
                    "title": "Default",
                    "id": "column-id-default",
                    "item": [{"id": "item-id-1", "title": "Item 1"}],
                },
                {
                    "title": "Column B",
                    "id": "column-id-2",
                    "item": [{"id": "item-id-2", "title": "Item 2"}],
                },
                {
                    "title": "Column C",
                    "id": "column-id-3",
                    "item": [{"id": "item-id-3", "title": "Item 3"}],
                },
                {
                    "title": "Column D",
                    "id": "column-id-4",
                    "item": [{"id": "item-id-4", "title": "Item 4"}],
                },
            ],
            "dragBoards": False,
            "element": f"#{kanban_element_id}",
        }
        context = {
            "kanban_options": kanban_options,
            "kanban_element_id": kanban_element_id,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        return self.model_admin.get_templates("kanban")

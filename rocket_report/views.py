from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):
    def get_kanban_data(self, context):
        return [
            {
                "id": "column-id-%s" % index,
                "item": [
                    {"id": "item-id-%s" % obj["pk"], "title": obj["title"],}
                    for index, obj in enumerate(
                        [
                            {"pk": index + 1, "title": "%s Item 1" % column},
                            {"pk": index + 2, "title": "%s Item 2" % column},
                            {"pk": index + 3, "title": "%s Item 3" % column},
                        ]
                    )
                ],
                "title": column,
            }
            for index, column in enumerate(["column a", "column b", "column c"])
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # replace object_list in context as we do not want it to be paginated
        context["object_list"] = self.queryset

        # see: https://github.com/riktar/jkanban#var-kanban--new-jkanbanoptions
        context["kanban_options"] = {
            "addItemButton": False,
            "boards": self.get_kanban_data(context),
            "dragBoards": False,
            "dragItems": False,
        }

        return context

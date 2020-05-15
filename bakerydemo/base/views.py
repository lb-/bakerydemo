from django.contrib.admin.templatetags.admin_list import ResultList, result_headers
from django.template.loader import render_to_string

from wagtail.contrib.modeladmin.templatetags.modeladmin_tags import result_list
from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):
    def render_kanban_item_html(self, context, obj, **kwargs):

        kwargs["obj"] = obj
        kwargs["action_buttons"] = self.get_buttons_for_obj(obj)

        context.update(**kwargs)

        return render_to_string(
            "modeladmin/kanban_item.html", context, request=self.request,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        list_filter = self.list_filter

        request = self.request
        object_list = context["object_list"]

        result_data = result_list(context)
        values = result_data["results"]
        headers = result_data["result_headers"]

        kanban_element_id = "kanban"

        kanban_options = {
            "addItemButton": False,
            "boards": [
                {
                    "title": "Default",
                    "id": "column-id-default",
                    "item": [
                        {
                            "id": f"item-id-{obj.pk}",
                            "title": self.render_kanban_item_html(
                                context,
                                obj,
                                fields=[
                                    {"label": label, "value": values[index][idx]}
                                    for idx, label in enumerate(headers)
                                ],
                                headers=headers,
                                index=index,
                                values=values[index],
                            ),
                        }
                        for index, obj in enumerate(object_list)
                    ],
                },
                {
                    "title": "Column B",
                    "id": "column-id-2",
                    "item": [{"id": "item-id-2", "title": "Item 2"}],
                },
                {
                    "title": "Column C",
                    "id": "column-id-3",
                    "item": [
                        {
                            "id": "item-id-3",
                            "title": "Test",
                        }
                    ],
                },
                {
                    "title": "Column D",
                    "id": "column-id-4",
                    "item": [{"id": "item-id-4", "title": "Item 4"}],
                },
            ],
            "dragBoards": False,
            "dragItems": False,
            "element": f"#{kanban_element_id}",
        }

        context["kanban_options"] = kanban_options
        context["kanban_element_id"] = kanban_element_id

        return context

    def get_template_names(self):
        return self.model_admin.get_templates("kanban")

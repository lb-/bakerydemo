from django.contrib.admin.templatetags.admin_list import ResultList, result_headers
from django.template.loader import render_to_string
from django.db.models import CharField, Count, F, Value

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
        column_field = getattr(self.model_admin, "kanban_column_field", None)
        column_name_default = getattr(
            self.model_admin, "kanban_column_name_default", "Other"
        )

        column_key = "__column_name"

        # replace object_list in context as we do not want it to be paginated
        queryset = self.queryset.annotate(
            __column_name=F(column_field)
            if column_field
            else Value(column_name_default, output_field=CharField())
        )
        context["object_list"] = queryset

        result_data = result_list(context)
        values = result_data["results"]
        headers = result_data["result_headers"]

        kanban_element_id = "kanban"

        columns = (
            queryset.values(column_key)
            .order_by(
                F(column_key).asc(nulls_first=True) if column_field else column_key
            )
            .annotate(count=Count("pk"))  # must be pk as value could be blank
        )

        items = [
            {
                "column": getattr(obj, column_key),
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
            for index, obj in enumerate(queryset)
        ]

        boards = [
            {
                "id": f"column-id-{index}",
                "item": [
                    item for item in items if item["column"] == column[column_key]
                ],
                # make into html?
                "title": "{column} ({count})".format(
                    **{
                        "count": column["count"],
                        "column": column.get(column_key, column_name_default)
                        or column_name_default,
                    }
                ),
            }
            for index, column in enumerate(columns)
        ]

        kanban_options = {
            "addItemButton": False,
            "boards": boards,
            "dragBoards": False,
            "dragItems": False,
            "element": f"#{kanban_element_id}",
        }

        # add kanban data to context
        context["kanban_options"] = kanban_options
        context["kanban_element_id"] = kanban_element_id

        return context

    def get_template_names(self):
        return self.model_admin.get_templates("kanban")

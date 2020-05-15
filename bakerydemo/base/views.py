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

        template = self.model_admin.get_kanban_item_template()

        return render_to_string(template, context, request=self.request,)

    def render_kanban_column_title_html(self, context, **kwargs):

        context.update(**kwargs)

        template = self.model_admin.get_kanban_column_title_template()

        return render_to_string(template, context, request=self.request,)

    def get_kanban_data(self, context):

        # prepare data used throughout based on context

        result_data = result_list(context)
        object_list = context["object_list"]
        values = result_data["results"]
        headers = result_data["result_headers"]

        # prepare column data
        column_field = self.model_admin.get_kanban_column_field()
        column_name_default = self.model_admin.get_kanban_column_name_default()

        column_key = "__column_name"

        queryset = object_list.annotate(
            __column_name=F(column_field)
            if column_field
            else Value(column_name_default, output_field=CharField())
        )

        order = F(column_key).asc(nulls_first=True) if column_field else column_key

        cols = queryset.values(column_key).order_by(order).annotate(count=Count("pk"))

        # set up items (for ALL columns)
        items = [
            {
                "column": getattr(obj, column_key),
                "id": "item-id-%s" % obj.pk,
                "title": self.render_kanban_item_html(
                    context,
                    obj,
                    fields=[
                        {"label": label, "value": values[index][idx]}
                        for idx, label in enumerate(headers)
                    ],
                ),
            }
            for index, obj in enumerate(queryset)
        ]

        # set up columns (aka boards) with sets of filtered items inside
        columns = [
            {
                "id": "column-id-%s" % index,
                "item": [
                    item for item in items if item["column"] == column[column_key]
                ],
                "title": self.render_kanban_column_title_html(
                    context,
                    count=column["count"],
                    name=column.get(column_key, column_name_default)
                    or column_name_default,
                ),
            }
            for index, column in enumerate(cols)
        ]

        return columns

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # replace object_list in context as we do not want it to be paginated
        context["object_list"] = self.queryset

        boards = self.get_kanban_data(context)

        # add kanban data to context
        context["kanban_options"] = {
            "addItemButton": False,
            "boards": boards,
            "dragBoards": False,
            "dragItems": False,
            "element": "#kanban",
        }

        context["kanban_element_id"] = "kanban"

        return context

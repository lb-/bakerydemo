import json

from django.contrib.admin.templatetags.admin_list import result_headers

from django.template.loader import render_to_string
from django.db.models import CharField, Count, F, Value

from wagtail.contrib.modeladmin.templatetags.modeladmin_tags import result_list
from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for form submission that contains one hidden (json) field 'changes'
        Parse the data supplied and supply to the the change_hander
        Note: Makes assumption that column orders are reasonably static
        """

        change_handler = self.model_admin.get_kanban_column_change_handler()
        if change_handler is None:
            return self.get(request, *args, **kwargs)

        changes = json.loads(request.POST.get("changes", "{}"))
        columns = self.get_kanban_columns()

        # gather the field that has been used to determine the column
        field = columns["field"]

        for key, change in changes.items():
            # convert {'item-id-22': ['column-id-0', 'column-id-5']}
            # to pk = '22', from = 'some value', to = 'some other value'
            pk = key.split("-")[-1]
            to = int(change[-1].split("-")[-1])
            column = columns["columns"][to]
            value = column.get(columns["key"], "")
            # allow the supplied change_handler to do the 'work' of reading and updating the instance
            change_handler(request, pk, field, value)

        return self.get(request, *args, **kwargs)

    def render_kanban_item_html(self, context, obj, **kwargs):
        """
        Allow for template based rendering of the content that goes inside each item
        Prepare action buttons that will be the same as the classic modeladmin index
        """

        kwargs["obj"] = obj
        kwargs["action_buttons"] = self.get_buttons_for_obj(obj)

        context.update(**kwargs)

        template = self.model_admin.get_kanban_item_template()

        return render_to_string(template, context, request=self.request,)

    def render_kanban_column_title_html(self, context, **kwargs):
        """
        Allow for template based rendering of the content that goes at the top of a column
        """

        context.update(**kwargs)

        template = self.model_admin.get_kanban_column_title_template()

        return render_to_string(template, context, request=self.request,)

    def get_kanban_columns(self):
        """
        Gather all column related data
        columns: name & count queryset
        default: label of a column that either has None value or does not exist on the field
        field: field name that is used to get the value from the instance
        key: internal use key to refer to the annotated column name label value
        queryset original queryset annotated with the column name label
        """
        object_list = self.queryset

        column_field = self.model_admin.get_kanban_column_field()
        column_name_default = self.model_admin.get_kanban_column_name_default()

        column_key = "__column_name"

        queryset = object_list.annotate(
            __column_name=F(column_field)
            if column_field
            else Value(column_name_default, output_field=CharField())
        )

        order = F(column_key).asc(nulls_first=True) if column_field else column_key

        columns = (
            queryset.values(column_key).order_by(order).annotate(count=Count("pk"))
        )

        return {
            "columns": columns,
            "default": column_name_default,
            "field": column_field,
            "key": column_key,
            "queryset": queryset,
        }

    def get_kanban_data(self, context):
        """
        Prepares the data that is used by the Kanban js library
        An array of columns, each with an id, title (html) and item
        Item value in each column contains an array of items which has a column, id & title (html)
        """
        columns = self.get_kanban_columns()

        # use existing model_admin utility to build headers/values
        result_data = result_list(context)

        # set up items (for ALL columns)
        items = [
            {
                "column": getattr(obj, columns["key"]),
                "id": "item-id-%s" % obj.pk,
                "title": self.render_kanban_item_html(
                    context,
                    obj,
                    fields=[
                        {"label": label, "value": result_data["results"][index][idx]}
                        for idx, label in enumerate(result_data["result_headers"])
                    ],
                ),
            }
            for index, obj in enumerate(columns["queryset"])
        ]

        # set up columns (aka boards) with sets of filtered items inside
        return [
            {
                "id": "column-id-%s" % index,
                "item": [
                    item for item in items if item["column"] == column[columns["key"]]
                ],
                "title": self.render_kanban_column_title_html(
                    context,
                    count=column["count"],
                    name=column.get(columns["key"], columns["default"])
                    or columns["default"],
                ),
            }
            for index, column in enumerate(columns["columns"])
        ]

    def get_context_data(self, **kwargs):
        # all the super's context first, so we can add to it and override some parts
        context = super().get_context_data(**kwargs)

        # get change_handler to determine if this board will allow drag/drop changes
        change_handler = self.model_admin.get_kanban_column_change_handler()

        # replace object_list in context as we do not want it to be paginated
        context["object_list"] = self.queryset

        # add kanban data to context
        # see: https://github.com/riktar/jkanban#var-kanban--new-jkanbanoptions
        context["kanban_options"] = {
            "addItemButton": False,
            "boards": self.get_kanban_data(context),
            "dragBoards": False,
            "dragItems": change_handler is not None,
        }

        return context

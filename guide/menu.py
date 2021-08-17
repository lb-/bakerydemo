from django.utils.html import format_html

from wagtail.contrib.modeladmin.menus import ModelAdminMenuItem

from .models import Guide


class GuideAdminMenuItem(ModelAdminMenuItem):
    def get_context(self, request):
        context = super().get_context(request)

        data = Guide.get_data_for_request(request)

        if data:

            context["attr_string"] = format_html('data-help="{}"', data["value_json"])
            context["classnames"] = context["classnames"] + " help-available"

        return context

from django import template

from wagtail.images.models import Image

register = template.Library()


@register.inclusion_tag("tags/form_fieldset.html", takes_context=True)
def fieldset(context, fields, label, description, form):
    print("fieldset tag", fields, label, description, form)

    return {
        "description": description,
        "fields": [form[field] for field in fields],
        "form": form,
        "label": label,
    }

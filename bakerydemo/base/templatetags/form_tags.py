from django import template

register = template.Library()


@register.inclusion_tag("tags/form_fieldset.html")
def fieldset(fieldset, form):
    return {
        "description": fieldset.get("help_text", None),
        "fields": [form[field] for field in fieldset.get("fields", [])],
        "form": form,
        "label": fieldset.get("label", None),
    }

from django import template

register = template.Library()


@register.filter(name='filter_with_permissions')
def filter_with_permissions(collections, user):
    """ filter the collections based on current user """
    return collections.filter(name__startswith='B')  # actual filter to be done

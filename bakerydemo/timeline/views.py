from django.shortcuts import render

from wagtail.admin.forms.search import SearchForm


def timeline_view(request):

    return render(request, "timeline.html", {
        'icon': 'time',
        'search_form': SearchForm(),
        'search_url': 'timeline',  # url name set by wagtail_hooks
        'title': 'Timeline'
    })

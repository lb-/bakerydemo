from django.shortcuts import render

from wagtail.admin.forms.search import SearchForm


def timeline_view(request):
    # Search
    query_string = None
    if 'q' in request.GET:
        search_form = SearchForm(request.GET, placeholder='Search timeline')
        if search_form.is_valid():
            query_string = search_form.cleaned_data['q']
    else:
        search_form = SearchForm(placeholder='Search timeline')

    return render(request, "timeline.html", {
        'icon': 'time',
        'query_string': query_string or '',
        'search_form': search_form,
        'search_url': 'timeline',  # url name set by wagtail_hooks
        'title': 'Timeline',
    })

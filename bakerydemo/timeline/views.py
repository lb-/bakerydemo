# timeline/views.py

from django.shortcuts import render


def timeline_view(request):

    return render(request, "timeline.html", {
        'title': 'Timeline',
    })

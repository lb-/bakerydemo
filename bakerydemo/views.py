from django.template.response import TemplateResponse

from wagtail.admin.modal_workflow import render_modal_workflow


def modal_view(request):
    
    return render_modal_workflow(
        request,
        'base/modal.html', # html template
        None, # js template
        {'trigger': request.GET.get('trigger')}, # html template vars
        json_data={'some': 'data'} # js template data
    )

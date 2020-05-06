# from django import template
# from bakerydemo.base.models import MyAppSettings

# register = template.Library()

# # reminder - you will need to restart Django when adding a template tag


# @register.inclusion_tag('tags/form_modal.html', takes_context=True)
# def form_modal(context):
#     request = context['request']  # important - you must have the request in context
#     settings = MyAppSettings.for_request(request)
#     form_page = settings.modal_form_page.specific

#     # this will provide the parts needed to render the form
#     # this does NOT handle the submission of the form - that still goes to the form page
#     # this does NOT handle anything to do with rendering the 'thank you' message

#     context['page'] = form_page
#     context['form'] = form_page.get_form(page=form_page, user=request.user)

#     return context

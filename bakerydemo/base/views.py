from django import forms
from django.core.exceptions import PermissionDenied

from wagtail.admin.forms.pages import CopyForm
from wagtail.admin.views import pages
from wagtail.core.models import Page


# BEGIN monkey patch of CopyForm
# See: wagtail/admin/forms/pages.py

original_form_init = CopyForm.__init__
original_form_clean = CopyForm.clean


def custom_form_init(self, *args, **kwargs):
    # note - the template will need to be overridden to show additional fields

    original_form_init(self, *args, **kwargs)
    self.fields['other'] = forms.CharField(initial="will fail", label="Other", required=False)


def custom_form_clean(self):
    cleaned_data = original_form_clean(self)

    other = cleaned_data.get('other')
    if other == 'will fail':
        self._errors['other'] = self.error_class(["This field failed due to custom form validation"])
        del cleaned_data['other']

    return cleaned_data


CopyForm.__init__ = custom_form_init
CopyForm.clean = custom_form_clean

# END monkey patch of CopyForm


def customCopy(request, page_id):
    """
    here we can inject any custom code for the response as a whole
    the template is a view function so we cannot easily customise it
    we can respond to POST or GET with any customisations though
    See: wagtail/admin/views/pages.py
    """

    page = Page.objects.get(id=page_id)

    # Parent page defaults to parent of source page
    parent_page = page.get_parent()

    # Check if the user has permission to publish subpages on the parent
    can_publish = parent_page.permissions_for_user(request.user).can_publish_subpage()

    # Create the form
    form = CopyForm(request.POST or None, user=request.user, page=page, can_publish=can_publish)

    if request.method == 'POST':
        if form.is_valid():
            # if the form has been validated (using the form clean above)
            # we get another chance here to fail the request, or redirect to another page
            # we can also easily access the specific page's model for any Page model methods
            try:
                if not page.specific.can_copy_check():
                    raise PermissionDenied
            except AttributeError:
                # continue through to the normal behaviour
                pass

    response = pages.copy(request, page_id)

    return response

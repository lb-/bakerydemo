from django.shortcuts import redirect
from django.urls import reverse

from wagtail.admin import messages
from wagtail.admin.views.generic import DeleteView
from wagtail.core.models import Page


class ArchiveView(DeleteView):
    delete_url_name = "archive"
    header_icon = "placeholder"
    index_url_name = "wagtailadmin_home"  # look at "archive_index" future
    model = Page
    edit_url_name = "wagtailadmin_pages:edit"
    page_title = "Archive page"
    success_message = "Page '{0}' has been archived."
    template_name = "base/archive/archive_confirm.html"

    @property
    def get_edit_url(self):
        return reverse(self.edit_url_name, args=(self.kwargs["pk"],))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("archive! GO", self.object)
        messages.success(request, self.get_success_message())
        return redirect(reverse(self.index_url_name))

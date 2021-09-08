from datetime import datetime

from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse

from wagtail.admin import messages
from wagtail.admin.views.generic import DeleteView
from wagtail.core.models import Page, PageLogEntry


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

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        Does not consider children just yet.
        """

        page = self.get_object()
        user = request.user

        self.object = page

        """
        1. unpublish page
        2. FUTURE: children!
        3. add archived_on value
        need to consider in progress workflows also maybe?
        """

        page.archived_on = datetime.now()
        page.unpublish(user=user)

        # need to register this
        PageLogEntry.objects.log_action(
            instance=page,
            action="archive",
            user=user,
        )

        page.save()

        print("archive! GO", self.object)
        messages.success(request, self.get_success_message())
        return redirect(reverse(self.index_url_name))

from django.contrib.admin.utils import quote
from django.urls import reverse

from generic_chooser.widgets import AdminChooser

from wagtail.documents.models import Document


class RestrictedDocumentChooser(AdminChooser):
    def __init__(self, **kwargs):

        self.accept = kwargs.pop("accept")

        super().__init__(**kwargs)

    choose_one_text = "Choose a Document"
    choose_another_text = "Choose another document"
    link_to_chosen_text = "Edit this document"
    model = Document
    choose_modal_url_name = "restricted_document_chooser:choose"

    def get_choose_modal_url(self):
        url = super().get_choose_modal_url()
        return url + "?accept=%s" % self.accept

    def get_edit_item_url(self, item):
        return reverse("wagtaildocs:edit", args=[item.id])

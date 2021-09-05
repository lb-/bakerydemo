from generic_chooser.views import ModelChooserViewSet

from wagtail.documents.models import Document


class RestrictedDocumentChooserViewSet(ModelChooserViewSet):
    icon = "document"
    model = Document
    page_title = "Choose a document"
    per_page = 10
    order_by = "title"
    fields = ["title", "file"]

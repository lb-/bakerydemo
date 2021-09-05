from django.db.models import Q

from generic_chooser.views import ModelChooserMixin, ModelChooserViewSet

from wagtail.documents.models import Document


class RestrictedDocumentChooserMixin(ModelChooserMixin):
    # preserve this URL parameter on pagination / search
    preserve_url_parameters = [
        "accept",
    ]

    def get_unfiltered_object_list(self):
        objects = super().get_unfiltered_object_list()

        accept = self.request.GET.get("accept")
        print("get_unfiltered_object_list", accept)

        if accept:
            accepted_files = accept.split(",")

            queries = [Q(file__iendswith=f".{value}") for value in accepted_files]

            query = queries.pop()
            for item in queries:
                query |= item

            objects = objects.filter(query)
        return objects


class RestrictedDocumentChooserViewSet(ModelChooserViewSet):
    chooser_mixin_class = RestrictedDocumentChooserMixin

    icon = "document"
    model = Document
    page_title = "Choose a document"
    per_page = 10
    order_by = "title"
    fields = ["title", "file"]

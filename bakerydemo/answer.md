Using [`wagtail-generic-chooser`](https://github.com/wagtail/wagtail-generic-chooser) offers much more ability to customise the way the Chooser modal works.

## Step 1 - Install `wagtail-generic-chooser`

- Run: `pip install wagtail-generic-chooser`
- Then add `generic_chooser` to your project's `INSTALLED_APPS`.

## Step 2 - Set up the Chooser view set

- Similar to the docs instructions on [setting up a Chooser view set](https://github.com/wagtail/wagtail-generic-chooser#chooser-views-model-based)
- Ensure we can handle the `accept` parameter by creating a custom class that extends the `ModelChooserMixin`, this will mean the param still gets passed when searching.
- Add handling of a `accept` URL param to conditionally filter the returned values.
- Set up a class that extends `ModelChooserViewSet` which will handle the showing of the `Document` listing within the modal.

#### **base/views.py**

```python
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

    icon = "doc"
    model = Document
    page_title = "Choose a document"
    per_page = 10
    order_by = "title"
    fields = ["title", "file"]

```

## Step 3 - Create the Chooser Widget

- This widget is not the `Block` but will be used as the base for the `Block` and can also be used for a `FieldPanel`.
- Similar to the [Setting up of a model based Widget](https://github.com/wagtail/wagtail-generic-chooser#chooser-widgets-model-based) create a class that extends the `AdminChooser`.
- In the `__init__` method we pull out the `accept` kwarg so we can use it to generate the custom URL param.
- Override the `get_edit_item_url` method which will allow the clicking of a _selected_ Document to edit it.
- Override the ``get_choose_modal_url` to append the URL query param (note: I could not get `reverse` working here without heaps more wrangling).

#### **base/models.py**

```python
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

```

## Step 4 - Register the chooser viewset in Wagtail Hooks

- No need to use the `construct_document_chooser_queryset` here, instead use the hook `register_admin_viewset` and register the `RestrictedDocumentChooserViewSet`.

#### **base/wagtail_hooks.py**

```python
from wagtail.core import hooks
from .views import RestrictedDocumentChooserViewSet

# ... other hooks etc

@hooks.register("register_admin_viewset")
def register_restricted_document_chooser_viewset():
    return RestrictedDocumentChooserViewSet(
        "restricted_document_chooser", url_prefix="restricted-document-chooser"
    )

```

## Step 5 - Set up and use the custom `Block`

- This class extends the `ChooserBlock` and wraps the `RestrictedDocumentChooser` widget that has been created.
- On `__init__` the same kwarg `accept` is pulled out and passed to the `RestrictedDocumentChooser` when created.
- This block can be used by calling it similar to any other block, with the kwarg `accept` though. `doc_block = RestrictedDocumentChooserBlock(accept="svg,md")`

```
from django.utils.functional import cached_property
from wagtail.images.blocks import ChooserBlock

# ...

class RestrictedDocumentChooserBlock(ChooserBlock):
    def __init__(self, **kwargs):
        self.accept = kwargs.pop("accept")
        super().__init__(**kwargs)

    @cached_property
    def target_model(self):
        from wagtail.documents.models import Document

        return Document

    @cached_property
    def widget(self):
        from .widgets import RestrictedDocumentChooser

        return RestrictedDocumentChooser(accept=self.accept)

    def get_form_state(self, value):
        return self.widget.get_value_data(value)

```

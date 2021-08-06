# How to create a Kanban (Trello style) view of your ModelAdmin data in Wagtail

**Goal: Create a ModelAdmin mixin that will make it easy to show an index view as a Kanban board.**

**Why:** Visual presentation is very helpful for planning and also a high-level understanding of information. Kanban boards provide a recognisable way to show sets of items in columns that represent their 'status' or grouping.

**How:** We want this to be as simple as possible, leveraging existing ModelAdmin conventions where possible and keeping as much of the logic being on the server. Drag & drop would be great but happy to sacrifice real-time / async Javascript behaviour to gain simplicity.

Inspiration: Kanban, notion.so, Trello, Github & Gitlab Kanban interface.

## Getting Started

Versions

- Wagtail 2.14
- Python 3.6
- Django 3.2
- jkanban 1.3 (Javascript/npm library)

Key Parts to Understand

- Terminology
- ModelAdmin (Wagtail's not Django's)
- Class Mixin

## Tutorial

### 1. Prepare a ModelAdmin model

For this tutorial we will be using [ArsTechnica](https://arstechnica.com)'s [Rocket Report](https://arstechnica.com/newsletters/?subscribe=248910) as inspiration. As of writing the latest report was [Rocket Report: Super Heavy lights up](https://arstechnica.com/science/2021/07/rocket-report-super-heavy-lights-up-china-tries-to-recover-a-fairing/).

This regular post contains a `title`, `byline`, `preamble`, a `reports` section which breaks up the news snippets into class of launch (small, medium and large). At the end of the report there, is a small `timeline` of upcoming launches. The part we want to focus on for this tutorial is the `reports` section, and [Wagtail's snippets](https://docs.wagtail.io/en/stable/topics/snippets.html) are a perfect way to store this kind of related content in a centralised way.

#### Create app

We assume you already have a Wagtail application up and running, so our first step will be to find a place to store all our custom logic and models. We will [start a new app](https://docs.djangoproject.com/en/3.0/ref/django-admin/#startapp) called `rocket_report`.

1. Run `django-admin startapp rocket_report`
2. Update your `settings.py`

```python
INSTALLED_APPS = [
  # ...
  'rocket_report',
  # ... wagtail & django items
]
```

There will now be an app folder `rocket_report` with models, views, etc.

#### Create page Model

Our next step will be to define our `RocketReportPage` [page model](https://docs.wagtail.io/en/stable/topics/pages.html).

1. Add a page model to your `models.py` file, code example below.
2. Run `./manage.py makemigrations` & `./manage.py migrate`
3. Restart the dev server to validate that we can now add a Rocket Report Page in Wagtail's admin
4. Add one page for use throughout the rest of the tutorial

```python
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel


class RocketReportPage(Page):

    # Database fields
    byline = models.CharField(blank=True, max_length=120)
    preamble = RichTextField(blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel("byline"),
        FieldPanel("preamble", classname="full"),
        ImageChooserPanel("main_image"),
        # TBC - reports
        InlinePanel("related_launches", label="Timeline"),
    ]


class Launch(Orderable):
    page = ParentalKey(
        RocketReportPage, on_delete=models.CASCADE, related_name="related_launches"
    )
    date = models.DateField("Launch date")
    details = models.CharField(max_length=255)

    panels = [
        FieldPanel("date"),
        FieldPanel("details"),
    ]
```

#### Create snippet Model

Our rocket report items will be [Wagtail Snippets](https://docs.wagtail.io/en/stable/topics/snippets.html), this gives a simple way to edit, manage and select these items for our pages.

1. Add the snippet model to your same `models.py` file, code example below.
2. Run `./manage.py makemigrations` & `./manage.py migrate`
3. Restart the dev server to validate that we can now add the snippet in Wagtail's admin
4. Add some snippet entries for use throughout the rest of the tutorial

```python
from django.db import models
# ... include existing imports from model.py
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import FieldPanel


class RocketReportPage(Page):
    # ...
    content_panels = Page.content_panels + [
        # ... other field panels
        ImageChooserPanel("main_image"),
        # ... other field panels
    ]


@register_snippet
class RocketReport(models.Model):

    STATUS_CHOICES = [
        ("SUBMITTED", "Submitted"),
        ("REVIEWED", "Reviewed"),
        ("PROPOSED", "Proposed"),
        ("HOLD", "Hold"),
        ("CURRENT", "Current"),
    ]

    CATEGORY_CHOICES = [
        ("BLANK", "Uncategorised"),
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large"),
    ]

    submitted_url = models.URLField(null=True, blank=True)
    submitted_by = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True, choices=STATUS_CHOICES)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    category = models.CharField(
        max_length=255, choices=CATEGORY_CHOICES, default="BLANK"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("status"),
        FieldPanel("category"),
        FieldPanel("content"),
        FieldPanel("submitted_url"),
        FieldPanel("submitted_by"),
    ]

    def __str__(self):
        return self.title


class RocketReportPageReportPlacement(Orderable, models.Model):
    page = ParentalKey(
        RocketReportPage, on_delete=models.CASCADE, related_name="rocket_reports"
    )
    rocket_report = models.ForeignKey(
        RocketReport, on_delete=models.CASCADE, related_name="+"
    )

    panels = [
        SnippetChooserPanel("rocket_report"),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.rocket_report.title

```

#### Register with ModelAdmin

Now we can register the report model using [`ModelAdmin`](https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/index.html). Note that this is Wagtail's ModelAdmin not Django's.

1. Add `wagtail.contrib.modeladmin` to your `INSTALLED_APPS` in your `settings.py`
2. Add a new `ModelAdmin` class in admin.py, code example below.
3. Register this class in a new file `wagtail_hooks.py`, code example below.
4. Validate that we now have an admin sidebar item for 'Rocket Reports' which will show the default ModelAdmin item list.

```python
# admin.py
from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import RocketReport


class RocketReportAdmin(ModelAdmin):
    model = RocketReport
    menu_icon = "fa-rocket"
    list_display = ("title", "status", "category", "submitted_by")
    list_filter = ("status", "category")
    search_fields = ("title", "status", "category", "submitted_by")

```

```python
# wagtail_hooks.py
from wagtail.contrib.modeladmin.options import modeladmin_register

from .admin import RocketReportAdmin

modeladmin_register(RocketReportAdmin)

```

### 2. Create a template, view & mixin

We are going to now set up a custom `KanbanMixin` that will house the customisations to our `ModelAdmin`. We could put all of these customisations directly on our `RocketReportAdmin` but we want to set up something reusable. It would be good to have a basic understanding of how to [customise the index view (listing)](https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/indexview.html) before reading on.

#### Create Kanban index template

We will be using a Javascript library to do the client-side rendering and handling of interaction for our basic Kanban board. There are a lot of [Kanban JS libraries on Github](https://github.com/topics/kanban?l=javascript) and a few [Kanban packages on NPM](Kanban packages on NPM).

The package we will use is [Jkanban](https://www.riccardotartaglia.it/jkanban/), it has a simple API and does not rely on third-party dependencies. For simplicity, we will use the jsdelivr service to provide our script and CSS, find the package and use the [dist directory to get your script and style tags](https://www.jsdelivr.com/package/npm/jkanban?path=dist).

1. Create a template file `/templates/modeladmin/kanban_index.html`
2. To inherit the existing modeladmin index listing layout (header, search bar, title etc) add `{% extends "modeladmin/index.html" %}` at the top
3. The content blocks we will use, provided by the above template are `extra_css`, `extra_js` and `content_main`.
4. Remember to add `{{ block.super }}` to the js & css blocks so that existing scripts and styles will be used.
5. `content_main` block - add a div that will contain the Kanban with class `kanban-wrapper listing` and an inner div with an id `kanban-mount` which is used by JKanban to add the rendered kanban board
6. `extra_css` block - Add the `link` tag from jsdelivr and some basic styles within a `<style>` tag, in the code below we are starting with some margins and handling of longer boards
7. `extra_js` block - our goal is to simply load up some dummy data based on the [options docs for jKanban](https://github.com/riktar/jkanban#var-kanban--new-jkanbanoptions)

```javascript
document.addEventListener("DOMContentLoaded", function () {
  var options = {
    boards: [
      {
        id: "column-0",
        title: "Column A",
        item: [
          { id: "item-1", title: "Item 1" },
          { id: "item-2", title: "Item 2" },
          { id: "item-1", title: "Item 3" },
        ],
      },
      {
        id: "column-1",
        title: "Column B",
        item: [
          { id: "item-4", title: "Item 4" },
          { id: "item-5", title: "Item 4" },
          { id: "item-5", title: "Item 6" },
        ],
      },
    ],
  };

  // build the kanban board with supplied options
  var kanban = new jKanban(
    Object.assign({}, options, { element: "#kanban-mount" })
  );
});
```

##### Full template code

```html
{% extends "modeladmin/index.html" %}
{% comment %} templates/modeladmin/kanban_index.html {% endcomment %}

{% block extra_css %}
    {{ block.super }}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jkanban@1/dist/jkanban.min.css">
    <style>
      .kanban-wrapper {
        width: 100%;
        overflow-x: auto; /* add horizontal scrolling for wide boards */
        margin-top: 1rem;
        margin-bottom: 1rem;
      }

      .kanban-item {
        min-height: 4rem;
      }
    </style>
{% endblock %}

{% block extra_js %}
  {{ block.super }}
  <script src="https://cdn.jsdelivr.net/npm/jkanban@1/dist/jkanban.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      var options = {
        boards: [
          {
            id: 'column-0',
            title: 'Column A',
            item: [{ id: 'item-1', title: 'Item 1'}, { id: 'item-2', title: 'Item 2'}, { id: 'item-1', title: 'Item 3'}]}
          ,
          {
            id: 'column-1',
            title: 'Column B',
            item: [{ id: 'item-4', title: 'Item 4'}, { id: 'item-5', title: 'Item 4'}, { id: 'item-5', title: 'Item 6'}]
          }
        ]
      };

      // build the kanban board with supplied options
      // see: https://github.com/riktar/jkanban#var-kanban--new-jkanbanoptions
      var kanban = new jKanban(Object.assign({}, options, {element: '#kanban-mount'}));
    });
  </script>
{% endblock %}

{% block content_main %}
  <div class="kanban-wrapper listing">
    <div id="kanban-mount"></div>
  </div>
{% endblock %}
```

#### Create Mixin with template override

A template is only good if we can get our `ModelAdmin` to use it when rendering the index listing view instead of the default. We can leverage a mixin approach to override the `ModelAdmin` methods while still honouring the [existing config on a per app or model basis](https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/primer.html#overriding-templates).

1. We will store our mixin in the `admin.py` file.
2. `ModelAdmin` uses a method `get_index_template` to get the index listing template, simply override this to call the defined `index_template_name` or `get_templates("kanban_index")`.
3. This will ensure that the template made above will be found at `templates/modeladmin/kanban_index.html`
4. Be sure to add the mixin to your `RocketReportAdmin` class, before the `ModelAdmin` usage.

```python
# rocket_report/admin.py

class KanbanMixin:
    def get_index_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return self.index_template_name or self.get_templates("kanban_index")


class RocketReportAdmin(KanbanMixin, ModelAdmin):
    model = RocketReport
    # ...
```

#### Create View to supply mock data to the kanban board

Our goal is to keep as much logic on the server, so we need a way to provide the board data from our Django view to our client. Doing this comes with some issues of encoding/decoding and ensuring that server generated content cannot inject Javascript.

Thankfully, Django helps us out with its builtin tag [`json_script`](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#json-script) which provides a way for sever generated content to be provided to JS in a view in a safe way.

1. Add a new view to the app's `views.py` called `KanbanView`
2. This view will inherit the modeladmin `wagtail.contrib.modeladmin.views.IndexView`
3. Override `get_context_data`, calling super and then adding `kanban_options` with similar dummy data that we used in the template
4. Use this `KanbanView` within the `KanbanMixin`
5. Update the `kanban_index.html` to inject the JSON data via json-script

```python
# views.py
from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):
    def get_kanban_data(self, context):
        return [
            {
                "id": "column-id-%s" % index,
                "item": [
                    {"id": "item-id-%s" % obj["pk"], "title": obj["title"],}
                    for index, obj in enumerate(
                        [
                            {"pk": index + 1, "title": "%s Item 1" % column},
                            {"pk": index + 2, "title": "%s Item 2" % column},
                            {"pk": index + 3, "title": "%s Item 3" % column},
                        ]
                    )
                ],
                "title": column,
            }
            for index, column in enumerate(["column a", "column b", "column c"])
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # replace object_list in context as we do not want it to be paginated
        context["object_list"] = self.queryset

        # see: https://github.com/riktar/jkanban#var-kanban--new-jkanbanoptions
        context["kanban_options"] = {
            "addItemButton": False,
            "boards": self.get_kanban_data(context),
            "dragBoards": False,
            "dragItems": False,
        }

        return context
```


```python
# rocket_report/admin.py
from wagtail.contrib.modeladmin.options import ModelAdmin

from .views import KanbanView
from .models import RocketReport


class KanbanMixin:

    index_view_class = KanbanView

    def get_index_template(self):
        #...


class RocketReportAdmin(KanbanMixin, ModelAdmin):
    model = RocketReport
    # ...
```


```html
{% comment %} templates/modeladmin/kanban_index.html (just the JS block shown) {% endcomment %}
{% block extra_js %}
  {{ block.super }}
  <script src="https://cdn.jsdelivr.net/npm/jkanban@1/dist/jkanban.js"></script>
  {{ kanban_options|json_script:"kanban-options" }}
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      // load the options from server
      var options = JSON.parse(document.getElementById('kanban-options').textContent);
      console.log('loaded', { options })

      // build the kanban board with supplied options
      // see: https://github.com/riktar/jkanban#var-kanban--new-jkanbanoptions
      var kanban = new jKanban(Object.assign({}, options, {element: '#kanban-mount'}));
    });
  </script>
{% endblock %}
```

### 3. Render items columns from actual data

Our goal here is to finish this basic implementation by generating columns and items from the correct `Model`. To achieve this we will revise the `KanbanMixin` to have some methods for smaller templates (used for the title/content) and methods to determine what field will be used for the columns. After that, we can revise the View to prepare all the data.

#### Revise the KanbanMixin and add small templates

1. Add a method `get_kanban_item_template` to look for a template with the name `kanban_item` but also allow the Mixin usage to declare an attribute `kanban_item_template_name`. This way we can have simple defaults but allow each `KanbanMixin` to declare custom templates for the items on a per model basis.
2. Add a method `get_kanban_column_title_template` that is similar to the above but for the column title.
3. Add a method `get_kanban_column_field` which will return the first field name from the `list_filter` attribute on the Mixin usage, this means we can leverage the existing ModelAdmin attributes approach.
4. Finally, add a method `get_kanban_column_name_default` for a default column name, this will be used when there is no value for the Kanban column field (e.g. a drop-down where a None/blank value is selected).

```python
# rocket_report/admin.py

class KanbanMixin:
    index_view_class = KanbanView

    def get_index_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return self.index_template_name or self.get_templates("kanban_index")


    def get_kanban_item_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return getattr(
            self, "kanban_item_template_name", self.get_templates("kanban_item")
        )

    def get_kanban_column_title_template(self):
        # leverage the get_template to allow individual override on a per model basis
        return getattr(
            self,
            "kanban_column_title_template_name",
            self.get_templates("kanban_column_title"),
        )

    def get_kanban_column_field(self):
        # return a field to use to determine which column the item will be shown in
        # pull in the first value from list_filter if no specific column set
        list_filter = getattr(self, "list_filter", [])
        field = list_filter[0] if list_filter else None
        return field

    def get_kanban_column_name_default(self):
        # used for the column title name for None or no column scenarios
        return getattr(self, "kanban_column_name_default", "Other")
# ...
```

#### Revise the KanbanMixin and add small templates

There is a lot changed in this final step, the main methods added to the `KanbanView` are to generate all the various parts (columns/items) and use the template in each of those parts set up in the `KanbanMixin`.


1. Add a method `render_kanban_item_html` which will pull in the action buttons (part of `ModelAdmin`), the template and then pass all the data to the template from the `get_kanban_item_template` method. This will return a string (HTML) which will, in turn, be passed to the JSON data for the Kanban board.
2. Add a method `render_kanban_column_title_html` which will pass the context to the configured title template.
3. Add a method `get_kanban_columns` that uses a query which will gather ALL the Model instances and prepare the data which has groupings of those Models by their column, along with the columns (with their names) also.
4. Replace the method `get_kanban_data` with a series of List parsing that goes through the column data and prepares the items to be placed within each column in a format that, when converted to JSON, is suitable for jKanban.

```python
from django.contrib.admin.templatetags.admin_list import result_headers

from django.template.loader import render_to_string
from django.db.models import CharField, Count, F, Value

from wagtail.contrib.modeladmin.templatetags.modeladmin_tags import result_list
from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):

    def render_kanban_item_html(self, context, obj, **kwargs):
        """
        Allow for template based rendering of the content that goes inside each item
        Prepare action buttons that will be the same as the classic modeladmin index
        """

        kwargs["obj"] = obj
        kwargs["action_buttons"] = self.get_buttons_for_obj(obj)

        context.update(**kwargs)

        template = self.model_admin.get_kanban_item_template()

        return render_to_string(template, context, request=self.request,)

    def render_kanban_column_title_html(self, context, **kwargs):
        """
        Allow for template based rendering of the content that goes at the top of a column
        """

        context.update(**kwargs)

        template = self.model_admin.get_kanban_column_title_template()

        return render_to_string(template, context, request=self.request,)

    def get_kanban_columns(self):
        """
        Gather all column related data
        columns: name & count queryset
        default: label of a column that either has None value or does not exist on the field
        field: field name that is used to get the value from the instance
        key: internal use key to refer to the annotated column name label value
        queryset original queryset annotated with the column name label
        """
        object_list = self.queryset

        column_field = self.model_admin.get_kanban_column_field()
        column_name_default = self.model_admin.get_kanban_column_name_default()

        column_key = "__column_name"

        queryset = object_list.annotate(
            __column_name=F(column_field)
            if column_field
            else Value(column_name_default, output_field=CharField())
        )

        order = F(column_key).asc(nulls_first=True) if column_field else column_key

        columns = (
            queryset.values(column_key).order_by(order).annotate(count=Count("pk"))
        )

        return {
            "columns": columns,
            "default": column_name_default,
            "field": column_field,
            "key": column_key,
            "queryset": queryset,
        }

    def get_kanban_data(self, context):
        """
        Prepares the data that is used by the Kanban js library
        An array of columns, each with an id, title (html) and item
        Item value in each column contains an array of items which has a column, id & title (html)
        """
        columns = self.get_kanban_columns()

        # use existing model_admin utility to build headers/values
        result_data = result_list(context)

        # set up items (for ALL columns)
        items = [
            {
                "column": getattr(obj, columns["key"]),
                "id": "item-id-%s" % obj.pk,
                "title": self.render_kanban_item_html(
                    context,
                    obj,
                    fields=[
                        {"label": label, "value": result_data["results"][index][idx]}
                        for idx, label in enumerate(result_data["result_headers"])
                    ],
                ),
            }
            for index, obj in enumerate(columns["queryset"])
        ]

        # set up columns (aka boards) with sets of filtered items inside
        return [
            {
                "id": "column-id-%s" % index,
                "item": [
                    item for item in items if item["column"] == column[columns["key"]]
                ],
                "title": self.render_kanban_column_title_html(
                    context,
                    count=column["count"],
                    name=column.get(columns["key"], columns["default"])
                    or columns["default"],
                ),
            }
            for index, column in enumerate(columns["columns"])
        ]

    def get_context_data(self, **kwargs):
        # ... (same as before)
```

## Final Solution

* Code can be found [Github / lb-](https://github.com/lb-/bakerydemo/tree/tutorial/kanban-model-admin-ready/rocket_report)
* Screenshot

## Future Improvements & Feedback

* It took a while to get this published, so hopefully it all came together well but I would love any feedback and hope this is helpful to someone.
* Better handling of pre-setting 'values' for each item's field/value, currently renders inside `<td>` tags due to existing `ModelAdmin` assumptions.
* Handling drag & drop (even real-time) with column number updates and toast style messages, you can view a rough version of this in the repo above (see commit [ORIGINAL ROUGH IMPLEMENTATION](https://github.com/lb-/bakerydemo/commit/27edc8b48e91a7c90ae8f382b50368b32cddcd8a)).

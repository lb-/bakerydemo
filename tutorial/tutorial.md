# Creating a schematic editor within the Wagtail CMS with StimulusJS

## Goal

- Our goal is to create a way to present a product (or anything) visually alongside points over the image that aligns to a description.
- Often content like this has to be rendered fully as an image, see the [Instructables espresso machine article](https://www.instructables.com/How-to-use-an-espresso-machine-pulling-shots-st/) as an example.
- However, we want to provide a way to have the image and its labels in separate content, this means the content is more accessible, links can be provided to sub-content and the labels can be translated if needed. See the website for the [Aremde Nexus Prop coffee machine](https://aremde.com.au/nexus/nexus-pro/) as an example. Not only is this coffee machine amazing, made in Brisbane, Australia but their website has some nice pulsating 'dots' that can be hovered to show features of the machine.

![Aremde Coffee Machine website - example of our goal](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/t6ndf93dqki2z9qr6cqk.png)

## Our approach

A note on naming - Schematic - this can mean a few different things and maybe `diagram` would be more appropriate but we will go with `schematic` to mean the image along with some points with labels and `point` for the individual points that overlay the image.

1. Create a new Django app to contain the `schematic` model, we will design the model to contain the image and 'points' that align with the image.
2. Create a new Page that can add the Schematic and use Wagtail's built-in `InlinePanel` to allow for basic editing of these points.
3. Get the points and image showing in the page's template.
4. Refine the Wagtail CMS editing interface to firstly show the points visually over the image and then allow drag & drop positioning of the points all within the editor.

### Versions

- Python - 3.9
- [Django](https://docs.djangoproject.com/en/4.0/) - 4.0
- [Wagtail](https://docs.wagtail.org/en/stable/) - 2.16
- [Stimulus](https://stimulus.hotwired.dev/) - 3.0.1

## Assumptions

- You have a working Wagtail project running locally, either your own project or something like the [bakerydemo](https://github.com/wagtail/bakerydemo) project.
- You are using the `images` and `snippets` Wagtail apps (common in most installations).
- You have installed the [Wagtail API](https://docs.wagtail.org/en/stable/advanced_topics/api/index.html#wagtail-api) and have set up the URLs as per the basic configuration.
- You have a basic knowledge of Wagtail, Django, Python and JavaScript.

## Tutorial

## Part 1 - Create a new `schematics` app plus `Schematic` & `SchematicPoint` models

1. `python manage.py startapp schematics` - create a new Django application to house the models and assets.
2. Add `'schematics'` to your `INSTALLED_APPS` within your Django settings.
3. Create a [Wagtail snippet](https://docs.wagtail.org/en/stable/topics/snippets.html#id1) which will hold our `Schematic` and `SchematicPoint` models, code and explanation below.
4. Run `./manage.py makemigrations`, check the output matches expectations and then `./manage.py migrate` to migrate your local DB.
5. Restart your dev server `./manage.py runserver 0.0.0.0:8000` and validate that the new model is now available within the Snippets section accessible from the sidebar menu.
6. Now create a single Schematic snippet so that there is some test data to work with and so you get a feel for the editing of this content.

![Wagtail CMS Snippet editor setup](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/duo24ajq9ec1lcm71j09.png)

### Code - `models.py`

- We will create two models, `Schematic` and `SchematicPoint`, the first will be a Wagtail snippet using the `@register_snippet` decorator via `from wagtail.snippets.models import register_snippet`.
- The `Schematic` model has two fields `title` (a simple CharField) and `image` (a Wagtail image), the panels will also reference the related `points` model.
- The `SchematicPoint` model has a `ParentalKey` (from [modelcluster](https://github.com/wagtail/django-modelcluster)) which is included with Wagtail, for more information about this read the [`InlinePanel` & modelclusters section](https://docs.wagtail.org/en/stable/reference/pages/panels.html#inline-panels) of the Wagtail docs.
- The `SchematicPoint` also has an x and y coordinate (percentages), the reasoning of using percentages is that it maps well to scenarios where the image may change or image may be shown at various sizes, if we go to px we have to solve a whole bunch of problems that present themselves. We also use the `DecimalField` to allow for up to 2 decimal places of precision within the value, e.g. 0.01 through to 99.99. (We are using max digits 5 because technically 100.00 is valid).
- Note that we are using `MaxValueValidator`/`MinValueValidator` for the server-side validation of the values and `NumberInput` widget attrs for the client side (browser) validation. Django [widget attrs](https://docs.djangoproject.com/en/4.0/ref/forms/widgets/#django.forms.Widget.attrs) is a powerful way to add HTML attributes to the form fields without needing to dig into templates, we will use this more later.

```python
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
)
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Schematic(index.Indexed, ClusterableModel):
    title = models.CharField("Title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        ImageChooserPanel("image"),
        InlinePanel("points", heading="Points", label="Point"),
    ]

    def __str__(self):
        title = getattr(self, "title", "Schematic")
        return f"Schematic - {title} ({self.pk})"

    class Meta:
        verbose_name_plural = "Schematics"
        verbose_name = "Schematic"


class SchematicPoint(Orderable, models.Model):
    schematic = ParentalKey(
        "schematics.Schematic",
        on_delete=models.CASCADE,
        related_name="points",
    )

    label = models.CharField("Label", max_length=254)

    x = models.DecimalField(
        verbose_name="X →",
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
    )

    y = models.DecimalField(
        verbose_name="Y ↑",
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0)],
    )

    panels = [
        FieldPanel("label"),
        FieldRowPanel(
            [
                FieldPanel(
                    "x", widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0})
                ),
                FieldPanel(
                    "y", widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0})
                ),
            ]
        ),
    ]

    def __str__(self):
        schematic_title = getattr(self.schematic, "title", "Schematic")
        return f"{schematic_title} - {self.label}"

    class Meta:
        verbose_name_plural = "Points"
        verbose_name = "Point"

```

## Part 2 - Create a new `ProductPage` model that will use the `schematic` model

1. You may want to integrate this into an existing page but for the sake of the tutorial, we will create a simple `ProductPage` that will have a `ForeignKey` to our `Schematic` snippet.
2. The snippet will be selectable via the [`SnippetChooserPanel`](https://docs.wagtail.org/en/stable/reference/pages/panels.html#module-wagtail.snippets.edit_handlers) which provides a chooser modal where the snippet can be selected. This also allows the same `schematic` to be available across multiple instances of the `ProductPage` or even available in other pages and shared as a discrete bit of content.
3. Remember to run `./manage.py makemigrations`, check the output matches expectations and then `./manage.py migrate` to migrate your local DB.
4. Finally, be sure to create a new `ProductPage` in the Wagtail admin and link its schematic to the one created in step 1 to test the snippet chooser is working.

![Page model editing with Snippet Chooser](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i2dq5kyi6447s6bng61p.png)

### Code - `models.py`

```python
from django.db import models

from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class ProductPage(Page):

    schematic = models.ForeignKey(
        "schematics.Schematic",
        null=True,
        on_delete=models.SET_NULL,
        related_name="product_page_schematic",
    )

    content_panels = Page.content_panels + [SnippetChooserPanel("schematic")]

```

## Part 3 - Output the points over an image in the `Page`'s template

1. Now create a template to output the image along with the points, this is a basic template that gets the general idea across of using the point coordinates to position them over the image.
2. We will use the `wagtailimages_tags` to allow the rendering of an image at a specific size and the usage of the `self.schematic` within the template to get the points data.

![Published page with the points showing over the image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n0ebsbtzris61x2k2e1m.png)

### Code - `myapp/templates/schematics/product_page.html`

- The template below is built on the [bakerydemo](https://github.com/wagtail/bakerydemo), so there is a base template that is extended.
- Please note the CSS is not polished and will need to be adjusted to suit your own branding and desired hover behaviour.

```html+django
{% extends "base.html" %}
{% load wagtailimages_tags %}

{% block head-extra %}
  <style>
    .schematic {
      position: relative;
    }

    .schematic .points {
      margin-bottom: 0;
    }

    .schematic .point {
      position: absolute;
    }

    .schematic .point::before {
      background-color: #fb7575;
      border-radius: 50%;
      box-shadow: 0 -2px 0 rgba(0, 0, 0, 0.1) inset;
      content: "";
      display: block;
      border: 0.5rem solid transparent;
      height: 2.75rem;
      background-clip: padding-box; /* ensures the 'hover' target is larger than the visible circle */
      position: absolute;
      transform: translate(-50%, -50%);
      width: 2.75rem;
      z-index: 1;
    }

    .point .label {
      opacity: 0; /* hide by default */
      position: absolute;

      /* vertically center */
      top: 50%;
      transform: translateY(-50%);

      /* move to right */
      left: 100%;
      margin-left: 1.25rem; /* and add a small left margin */

      /* basic styles */
      font-family: sans-serif;
      width: 12rem;
      padding: 5px;
      border-radius: 5px;
      background: #000;
      color: #fff;
      text-align: center;
      transition: opacity 300ms ease-in-out;
      z-index: 10;
    }

    .schematic .point:hover .label {
      opacity: 1;
    }
  </style>
{% endblock head-extra %}

{% block content %}
  {% include "base/include/header.html" %}
  <div class="container">
    <div class="row">
      {% image self.schematic.image width-1920 as schematic_image %}
      <div class="schematic col-md-12">
        <img src="{{ schematic_image.url }}" alt="{{ schematic.title }}" />
        <ul class="points">
          {% for point in self.schematic.points.all %}
          <li class="point" style="left: {{ point.x }}%; bottom: {{ point.y }}%">
            <span class="label">{{ point.label }}</span>
          </li>
          {% endfor %}
        </ul>
      </div>
    </div>
  </div>
{% endblock content %}
```

## Part 4 - Enhance the editor's experience to show a different image size

- Before we can try to show the 'points' within the image in the editor we need to change the behaviour of the built-in [`ImageChooserPanel`](https://docs.wagtail.org/en/stable/reference/pages/panels.html#imagechooserpanel) to load a larger image when editing. This panel has two modes, editing an existing 'saved' value (shows the image on load) or updating an image by choosing a new one either for the first time or editing, this image is provided from the server.
- At this point we will start writing some JavaScript and use the Stimulus 'modest' framework, see the bottom of this article for a bit of a high-level overview of Stimulus if you have not yet heard about it. Essentially, Stimulus gives us a way to assign `data-` attributes to elements to link their behaviour to a `Controller` class in JavaScript and avoids a lot of the boilerplate usually needed when working with jQuery or vanilla (no framework) JS such as adding event listeners or targeting elements predictably.
- On the server-side we will create a sub-class of `ImageChooserPanel` which allows us to modify the size of the image that is returned if already saved and add our template overrides so we can update the HTML.
- We will break this part into a few sub-steps.

### Part 4a - Adding Stimulus via `wagtail_hooks`

- Wagtail provides a system of ['hooks'](https://docs.wagtail.org/en/stable/reference/hooks.html) where you can add a file `wagtail_hooks.py` to your app and it will be run by Wagtail on load.
- We will use the [`insert_editor_js`](https://docs.wagtail.org/en/stable/reference/hooks.html#id19) hook to add our JavaScript module.
- The JavaScript used from here on in assumes you are supporting browsers that have [`ES6`](https://caniuse.com/?search=es6) support and relies extensively on ES6 modules, arrow functions and classes.
- We will be installing Stimulus as an ES6 module in a similar way to the [Stimulus installation guide - without using a build system](https://stimulus.hotwired.dev/handbook/installing#using-without-a-build-system).

#### Create a new file `schematics/wagtail_hooks.py`

- Once created, stop your Django dev server and restart it (hooks will not run the first time after the file is added unless you restart).
- You can validate this step is working by checking the browser inspector - checking that the script module exists, remember this will only show on editing pages or editing models and not on the dashboard for example due to the Wagtail hook used.
- Assuming you are running Django with `DEBUG = True` in your dev server settings you should also see some console info about the status of Stimulus.

```python
from django.conf import settings
from django.utils.html import format_html

from wagtail.core import hooks


@hooks.register("insert_editor_js")
def insert_stimulus_js():
    return format_html(
        """
        <script type="module">
            import {{ Application, Controller }} from "https://unpkg.com/@hotwired/stimulus/dist/stimulus.js";
            const Stimulus = Application.start();
            {}
            window.dispatchEvent(new CustomEvent('stimulus:init', {{ detail: {{ Stimulus, Controller }} }}));
        </script>
        """,
        # set Stimulus to debug mode if running Django in DEBUG mode
        "Stimulus.debug = true;" if settings.DEBUG else "",
    )

```

### Part 4b - Creating `schematics/edit_handlers.py` with a custom `ImageChooserPanel`

1. Create a new file `schematics/edit_handlers.py`.
2. In this file we will sub-class the built-in `ImageChooserPanel` and its usage of `AdminImageChooser` to customise the behaviour via a new class `SchematicImageChooserPanel`.
3. `SchematicImageChooserPanel` extends `ImageChooserPanel` and does two things; it updates the `widget_overrides` to use a second custom class `AdminPreviewImageChooser` and passes down a special data attribute to the input field. This attribute is a [Stimulus `target` attribute](https://stimulus.hotwired.dev/reference/targets) and allows our JavaScript to easily access this field.
4. Within `AdminPreviewImageChooser` we override the `get_value_data` method to customise the image preview output, remember that this is only used when editing an existing model with a chosen image. We are using the [`get_rendition` method](https://docs.wagtail.org/en/stable/advanced_topics/images/renditions.html#image-renditions) built-in to Wagtail's `Image` model.
5. We also need to ensure we use the `SchematicImageChooserPanel` in our `models.py`.
6. Remember to validate before moving on, you can do this by checking the image that is loaded when editing a model that already has a chosen image, it should be a much higher resolution version.

```python
# schematics/edit_handlers.py
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.widgets import AdminImageChooser


class AdminPreviewImageChooser(AdminImageChooser):
    """
    Generates a larger version of the AdminImageChooser
    Currently limited to showing the large image on load only.
    """

    def get_value_data(self, value):
        value_data = super().get_value_data(value)

        if value_data:
            image = self.image_model.objects.get(pk=value_data["id"])
            # note: the image string here should match what is used in the template
            preview_image = image.get_rendition("width-1920")
            value_data["preview"] = {
                "width": preview_image.width,
                "height": preview_image.height,
                "url": preview_image.url,
            }

        return value_data


class SchematicImageChooserPanel(ImageChooserPanel):
    def widget_overrides(self):
        return {
            self.field_name: AdminPreviewImageChooser(
                attrs={
                    "data-schematic-edit-handler-target": "imageInput",
                }
            )
        }

```

```python
# schematics/models.py

# ... existing imports

from .edit_handlers import SchematicImageChooserPanel


@register_snippet
class Schematic(index.Indexed, ClusterableModel):

    # ...fields

    panels = [
        FieldPanel("title"),
        SchematicImageChooserPanel("image"), # ImageChooserPanel("image") - removed
        InlinePanel("points", heading="Points", label="Point"),
    ]


# .. other model - SchematicPoint

```

### Part 4c - Adding a custom `EditHandler`

- In Wagtail, there is a core class [`EditHandler`](https://docs.wagtail.org/en/stable/topics/pages.html?highlight=EditHandler#editor-panels) which contains much of the rendering of lists of containers/fields within a page and other editing interfaces (including snippets).
- So that we can get more control over how our `Schematic` editor is presented, we will need to create a sub-class of this called `SchematicEditHandler`.
- Our `SchematicEditHandler` will add some HTML around the built-in class and also provide the editor specific JS/CSS we need for this content. We could add the CSS/JS via more Wagtail Hooks but then it would load on every single editor page, even if the user is not editing the Schemas.

#### In the file `schematics/edit_handlers.py` create a custom `SchematicEditHandler`

- This new file (schematics/edit_handlers.py) will contain our custom editor handler classes, we will start with `SchematicEditHandler` which extends `ObjectList`.
- Using the `get_form_class` method we generate a [new dynamic class with the `type` function](https://www.geeksforgeeks.org/create-classes-dynamically-in-python/) that has a `Media` class within it.
- Django will use the [`Media` class on a `Form`](https://docs.djangoproject.com/en/4.0/topics/forms/media/#media-on-forms) to load any JS or CSS files declared but only once and only if the form is shown.

```python
# schematics/edit_handlers.py
from django.utils.html import format_html # this import is added

from wagtail.admin.edit_handlers import ObjectList # this import is added
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.widgets import AdminImageChooser

# ... other classes

class SchematicEditHandler(ObjectList):
    template = "schematics/edit_handlers/schematic_edit_handler.html"

    def get_form_class(self):
        form_class = super().get_form_class()
        return type(
            form_class.__name__,
            (form_class,),
            {"Media": self.Media},
        )

    class Media:
        css = {"all": ("css/schematic-edit-handler.css",)}
        js = ("js/schematic-edit-handler.js",)

```

#### Use the `SchematicEditHandler` on the `Schematic` model

- We will need to ensure we use this `SchematicEditHandler` in our `models.py`
- Once this is done, you can validate that it is working by reloading the Wagtail admin, editing an existing `Schematic` snippet and checking the network tools in the browser inspector. It should have tried to load the `schematic-edit-handler.css` & `schematic-edit-handler.js` files - which are not yet added - just check that the requests were made.

```python
# schematics/models.py

# ... existing imports

from .edit_handlers import (
    SchematicEditHandler,
    SchematicImageChooserPanel,
)


@register_snippet
class Schematic(index.Indexed, ClusterableModel):

    # ...fields

    # panels = [ ... put the edit_handler after panels

    edit_handler = SchematicEditHandler(panels)

# .. other model - SchematicPoint

```

### Part 4d - Adding initial JS & CSS for the schematic edit handler

#### Create `schematic-edit-handler.js` - Stimulus Controller

- This file will be a [Stimulus Controller](https://stimulus.hotwired.dev/reference/controllers) that gets created once the event `stimulus:init` fires on the window (added earlier by our `wagtail_hooks.py`).
- `static targets = [...` - this tells the controller to look at for a DOM element and 'watch' it to check if it exists or gets created while the controller is active. This will specifically look for the data attribute `data-schematic-handler-target="imageInput"` and make it available inside the Controller's instance.
- `connect` is a class method similar to `componentDidMount` in React or `x-init/init()` in Alpine.js - it essentially means that there is a DOM element available.
- Once connected, we call a method `setupImageInputObserver` which we have made in this class, it uses the [MutationObserver](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver) browser API to listen to the image's input value. The reason we cannot just use the `'change'` event is due to this value being updated programmatically, we also cannot easily listen to when the chooser modal closes as those are jQuery events that are not compatible with built-in browser events.
- Finally, once we know the image input (id) has changed and has a value (e.g. was not just cleared), we can fire of an API call to the internal Wagtail API to get the image path, this happens in the `updateImage` method. Once resolved, we update the `src` on the `img` tag.
- You can now validate this by refreshing and then changing an image to a new one via the image chooser, the newly loaded image should get updated to the full size variant of that image.

```js
// static/js/schematic-edit-handler.js
window.addEventListener("stimulus:init", ({ detail }) => {
  const Stimulus = detail.Stimulus;
  const Controller = detail.Controller;

  class SchematicEditHandler extends Controller {
    static targets = ["imageInput"];

    connect() {
      this.setupImageInputObserver();
    }

    /**
     * Once connected, use DOMMutationObserver to 'listen' to the image chooser's input.
     * We are unable to use 'change' event as it is updated by JS programmatically
     * and we cannot easily listen to the Bootstrap modal close as it uses jQuery events.
     */
    setupImageInputObserver() {
      const imageInput = this.imageInputTarget;

      const observer = new MutationObserver((mutations) => {
        const { oldValue = "" } = mutations[0] || {};
        const newValue = imageInput.value;
        if (newValue && oldValue !== newValue)
          this.updateImage(newValue, oldValue);
      });

      observer.observe(imageInput, {
        attributeFilter: ["value"],
        attributeOldValue: true,
        attributes: true,
      });
    }

    /**
     * Once we know the image has changed to a new one (not just cleared)
     * we use the Wagtail API to find the original image URL so that a more
     * accurate preview image can be updated.
     *
     * @param {String} newValue
     */
    updateImage(newValue) {
      const image = this.imageInputTarget
        .closest(".field-content")
        .querySelector(".preview-image img");

      fetch(`/api/v2/images/${newValue}/`)
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`HTTP error! Status: ${response.status}`);
        })
        .then(({ meta }) => {
          image.setAttribute("src", meta.download_url);
        })
        .catch((e) => {
          throw e;
        });
    }
  }

  // register the above controller
  Stimulus.register("schematic-edit-handler", SchematicEditHandler);
});
```

#### Create `static/css/schematic-edit-handler.css` styles

- This is a base starting point to get the preview image and the action buttons to stack instead of show inline, plus allow the image to get larger based on the actual image used.

```css
/* static/css/schematic-edit-handler.css */
/* preview image - container */

.schematic-edit-handler .image-chooser .chosen {
  padding-left: 0;
}

.schematic-edit-handler .image-chooser .preview-image {
  display: inline-block; /* ensure container matches image size */
  max-width: 100%;
  margin: 2rem 0;
  float: none;
  position: relative;
}

.schematic-edit-handler .image-chooser .preview-image img {
  max-height: 100%;
  max-width: 100%;
}
```

![Larger preview image used with the custom ImageChooser panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ja46c1kns2pm6queb5l2.png)

## Part 5 - Enhance the editor's experience to show point positioning

- In this next part, our goal is to have the `points` shown visually over the image.
- The styling here is very similar to the styling used in our page template but we need to ensure that the points move when the inputs change.
- We will continue to expand on our Stimulus controller to house the JS behaviour and leverage another `data-` attribute around the InlinePanel used.
- Working with the `InlinePanel` (also called expanding formset) has some nuance, the main thing to remember is that these panels can be deleted but this deletion only happens visually as there are `input` fields under the hood that get updated. Also, the panels can be reordered and added at will.

### 5a - Add a `SchematicPointPanel` that will use a new template `schematics/edit_handlers/schematic_point_panel.html`

- We will update `schematics/edit_handlers.py` with another custom panel, this time extending the `MultiFieldPanel`, which is essentially just a thin wrapper around a bunch of fields.
- This custom class does one thing, point the panel to a new template.

```python
# schematics/edit_handlers.py
from django.utils.html import format_html

from wagtail.admin.edit_handlers import MultiFieldPanel, ObjectList # update - added MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.widgets import AdminImageChooser

# ... other classes

class SchematicPointPanel(MultiFieldPanel):
    template = "schematics/edit_handlers/schematic_point_panel.html"

```

- Create the new template `schematics/edit_handlers/schematic_point_panel.html` and all it does is wrap the existing multi_field_panel in a div that will add a class and add another Stimulus target.

```html+django
<div class="schematic-point-panel" data-schematic-edit-handler-target="point">
  {% extends "wagtailadmin/edit_handlers/multi_field_panel.html" %}
</div>
```

### 5b - Use the `SchematicPointPanel` in `models.py` & update `attrs`

- Now that we have created `SchematicPointPanel` we can use it inside our `SchematicPoint` model to wrap the `fields`.
- We have also reworked the various `FieldPanel` items to leverage the `widget` attribute so we can add some more data-attributes.
- Note that the `data-action` is a specific Stimulus attribute that says 'when this input changes fire a method on the Controller. It can be used to add specific event listeners as we will see later but the default behaviour on `input` elements is the `'change'` event.
- We also add some `data-point-` attributes, these are not Stimulus specific items but just a convenience attribute to find those elements in our Stimulus controller, we could use more `target` type attributes but that is not critical for the scope of this tutorial.
- A reminder that Django will smartly handle some attributes and when Python `True` is passed, it will be converted to a string `'true'` in HTML - thanks Django!

```python
# schematics/models.py
# ... imports

from .edit_handlers import (
    SchematicEditHandler,
    SchematicImageChooserPanel,
    SchematicPointPanel, # added
)

# Schematic model

class SchematicPoint(Orderable, models.Model):
    # schematic/label fields

    x = models.DecimalField(
        verbose_name="X →",
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
    )

    y = models.DecimalField(
        verbose_name="Y ↑",
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0)],
    )

    fields = [
        FieldPanel(
            "label",
            widget=forms.TextInput(
                attrs={
                    "data-action": "schematic-edit-handler#updatePoints",
                    "data-point-label": True,
                }
            ),
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "x",
                    widget=forms.NumberInput(
                        attrs={
                            "data-action": "schematic-edit-handler#updatePoints",
                            "data-point-x": True,
                            "min": 0.0,
                            "max": 100.0,
                        }
                    ),
                ),
                FieldPanel(
                    "y",
                    widget=forms.NumberInput(
                        attrs={
                            "data-action": "schematic-edit-handler#updatePoints",
                            "data-point-y": True,
                            "min": 0.0,
                            "max": 100.0,
                        }
                    ),
                ),
            ]
        ),
    ]

    panels = [SchematicPointPanel(fields)]

    # ... def/Meta

# other classes
```

### 5c - Add a `template` to `templates/schematics/edit_handlers/schematic_edit_handler.html`

- We need a way to determine how to output a `point` in the editor UI, and while we can build this up as a string in the Stimulus controller, let's make our lives easier to and use a [HTML `template` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template).
- This template will be pre-loaded with the relevant data attributes we need and a `label` slot to add the label the user has entered. The nice thing about this approach is that we can modify this rendering just by changing the HTML template later.

```html+django
<!-- templates/schematics/edit_handlers/schematic_edit_handler.html -->
<div class="schematic-edit-handler" data-controller="schematic-edit-handler">
  <template data-schematic-edit-handler-target="imagePointTemplate">
    <li
      class="point"
      data-schematic-edit-handler-target="imagePoint"
    >
      <span class="label"></span>
    </li>
  </template>
  {% extends "wagtailadmin/edit_handlers/object_list.html" %}
</div>
```

### 5d - Update the `SchematicEditHandler` Stimulus controller to output points

- In our Stimulus Controller we will add 4 new targets; `imagePoint` - shows the point visually over the preview images, `imagePoints` - container for the `imagePoint` elements, `imagePointTemplate` - the template to use, set in the above step, `point` - each related model added via the `InlinePanel` children.
- Now we can add a `pointTargetConnected` method, this is a powerful built-in part of the Stimulus controller where each target gets its [own connected/disconnected callbacks](https://stimulus.hotwired.dev/reference/targets#connected-and-disconnected-callbacks). These also fire when initially connected so we can have a consistent way to know what `InlinePanel` children exist on load AND any that are added by the user later without having to do too much of our own code here.
- `pointTargetConnected` basically adds a 'delete' button listener so we know when to re-update our points.
- `updatePoints` does the bulk of the heavy lifting here, best to read through the code line by line to understand it. Essentially it goes through each of the `point` targeted elements and builds up an array of elements based on the `imagePointTemplate` but only if that panel is not marked as deleted. It then puts those points into a `ul` element next to the preview image, which itself has a target of `imagePoints` to be deleted and re-written whenever we need to run another update.
- You should be able to validate this by reloading the page and seeing that there are a bunch of new elements added just under the image.

```js
// static/js/schematic-edit-handler.js

class SchematicEditHandler extends Controller {
    static targets = [
      "imageInput",
      "imagePoint",
      "imagePoints",
      "imagePointTemplate",
      "point",
    ];

    connect() {
      this.setupImageInputObserver();
      this.updatePoints(); // added
    }

    /**
     * Once a new point target (for each point within the inline panel) is connected
     * add an event listener to the delete button so we know when to re-update the points.
     *
     * @param {HTMLElement} element
     */
    pointTargetConnected(element) {
      const deletePointButton = element
        .closest("[data-inline-panel-child]")
        .querySelector('[id*="DELETE-button"]');

      deletePointButton.addEventListener("click", (event) => {
        this.updatePoints(event);
      });
    }

    // setupImageInputObserver() ...
    // updateImage() ...

    /**
     * Removes the existing points shown and builds up a new list,
     * ensuring we do not add a point visually for any inline panel
     * items that have been deleted.
     */
    updatePoints() {
      if (this.hasImagePointsTarget) this.imagePointsTarget.remove();

      const template = this.imagePointTemplateTarget.content.firstElementChild;

      const points = this.pointTargets
        .reduce((points, element) => {
          const inlinePanel = element.closest("[data-inline-panel-child]");
          const isDeleted = inlinePanel.matches(".deleted");

          if (isDeleted) return points;

          return points.concat({
            id: inlinePanel.querySelector("[id$='-id']").id,
            label: element.querySelector("[data-point-label]").value,
            x: Number(element.querySelector("[data-point-x]").value),
            y: Number(element.querySelector("[data-point-y]").value),
          });
        }, [])
        .map(({ id, x, y, label }) => {
          const point = template.cloneNode(true);
          point.dataset.id = id;
          point.querySelector(".label").innerText = label;
          point.style.bottom = `${y}%`;
          point.style.left = `${x}%`;
          return point;
        });

      const newPoints = document.createElement("ol");
      newPoints.classList.add("points");
      newPoints.dataset.schematicEditHandlerTarget = "imagePoints";

      points.forEach((point) => {
        newPoints.appendChild(point);
      });

      this.imageInputTarget
        .closest(".field-content")
        .querySelector(".preview-image")
        .appendChild(newPoints);
    }
//   rest of controller definition & registration
```

### 5e - Add styles for the points in `schematic-edit-handler.css`

- There is a fair bit of CSS happening here but our goal is to ensure that the points show correctly over the image and can be positioned absolutely.
- We also add a few nice visuals such as a label on hover, a number that shows in the circle and a number against each inline panel so that our users can mentally map these things easier.

```css
/* static/css/schematic-edit-handler.css */

/* preview image - container ...(keep as is) */

/* inline panels - add visible numbers */

.schematic-edit-handler .multiple {
  counter-reset: css-counter 0;
}

.schematic-edit-handler [data-inline-panel-child]:not(.deleted) {
  counter-increment: css-counter 1;
}

.schematic-edit-handler
  [data-inline-panel-child]:not(.deleted)
  > fieldset::before {
  content: counter(css-counter) ". ";
}

/* preview image - points */
/* tooltip styles based on https://blog.logrocket.com/creating-beautiful-tooltips-with-only-css/ */

.schematic-edit-handler .image-chooser .preview-image .points {
  counter-reset: css-counter 0;
}

.schematic-edit-handler .image-chooser .preview-image .point {
  counter-increment: css-counter 1;
  position: absolute;
}

.schematic-edit-handler .image-chooser .preview-image .point::before {
  background-clip: padding-box; /* ensures the 'hover' target is larger than the visible circle */
  background-color: #7c4c4c;
  border-radius: 50%;
  border: 0.25rem solid transparent;
  color: rgb(236, 236, 236);
  box-shadow: 0 -2px 0 rgba(0, 0, 0, 0.1) inset;
  content: counter(css-counter);
  text-align: center;
  line-height: 1.75rem;
  font-weight: bolder;
  display: block;
  height: 1.75rem;
  position: absolute;
  transform: translate(-50%, -50%);
  width: 1.75rem;
  z-index: 1;
}

.schematic-edit-handler .image-chooser .preview-image .point .label {
  opacity: 0; /* hide by default */
  position: absolute;

  /* vertically center */
  top: 50%;
  transform: translateY(-50%);

  /* move to right */
  left: 100%;
  margin-left: 1.25rem; /* and add a small left margin */

  /* basic styles */
  width: 5rem;
  padding: 5px;
  border-radius: 5px;
  background: #000;
  color: #fff;
  text-align: center;
  transition: opacity 300ms ease-in-out;
  z-index: 10;
}

.schematic-edit-handler .image-chooser .preview-image .point:hover .label {
  opacity: 1;
}
```

### 5f - Validation & congrats

- At this point, you should be able to load the Snippet with some existing points and once the JS runs see those points over the image.
- These points should align visually with the same points shown in the public-facing page (frontend) when that Schematic is used.
- Back in the Wagtail editor, we should be able to add/delete/reorder points with the `InlinePanel` UI and the points over the image should update each time.
- We should also be able to adjust the label, the number fields bit by bit and see the points also updated.
- Try to break it, see what does not work and what could be improved, but congratulate yourself for getting this far and learning something new!

![Final with points showing over the preview image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/idhz9el364z1u2tzowoq.png)

## Part 6 (Bonus) - Drag & Drop!

- If you want to go down the rabbit hole further, grab yourself a fresh shot of espresso or pour an Aeropress and sit down to make this editing experience even more epic.
- We will be using the [HTML Drag & Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API) here and it is strongly recommended you read through the MDN overview before proceeding.
- There are some caveats, we are working with a kind of lower-level API and there are browser support considerations to make.
- Ideally, we would pull in another library to do this for us but it is probably better to build it with plain old Vanilla JS first and then enhance it later once you know this is a good thing to work on.

### 6a - Add more data attributes to the point template

- At this point, you probably can tell that data attributes are our friend with Stimulus and Django so let's add some more.
- In `templates/schematics/edit_handlers/schematic_edit_handler.html` we will update our `template` (which gets used to generate the `li` point element).
- We have added `data-action="dragstart->schematic-edit-handler#pointDragStart dragend->schematic-edit-handler#pointDragEnd"` - this is the `data-action` from Stimulus showing off how powerful this abstraction is. Here we add two event listeners for specific events and no need to worry about `addEventListener` as it is done for us.
- We also add `draggable="true"` which is part of the HTML Drag & Drop API requirements.

```html
<div class="schematic-edit-handler" data-controller="schematic-edit-handler">
  <template data-schematic-edit-handler-target="imagePointTemplate">
    <li
      class="point"
      data-schematic-edit-handler-target="imagePoint"
      data-action="dragstart->schematic-edit-handler#pointDragStart dragend->schematic-edit-handler#pointDragEnd"
      draggable="true"
    >
      <span class="label"></span>
    </li>
  </template>
  {% extends "wagtailadmin/edit_handlers/object_list.html" %}
</div>
```

### 6b - Update the `SchematicEditHandler` Controller to handle drag / drop behaviour

- **Firstly**, we need to handle the drag (picking up) an element, these events are triggered by the `data-action` set above.
- `pointDragStart` - this will tell the browser that this element can 'move' and that we want to pass the `dataset.id` the eventual drop for tracking. We also make the element semi-transparent to show that it is being dragged, there are lots of other ways to visually show this but this is just a basic start.
- `pointDragEnd` - resets the style opacity back to normal.
- In the `connect` method we call a new method `setupImageDropHandlers`, this does the job of our `data-action` attributes but we cannot easily, without a larger set of Wagtail class overrides, add these attributes so we have to add the event handlers manually.
- `setupImageDropHandlers` - finds the preview image container and adds a listener for `'dragover'` to say 'this can drop here' and then the `'drop'` to do the work of updating the inputs.
- `addEventListener("drop"...` does a fair bit, essentially it pulls in the data from the drag behaviour, this helps us find what `InlinePanel` child we need to update. We then work out the x/y percentages of the dropped point relative to the image preview container and round that to 2 decimal places. The x/y values are then updated in the correct fields.
- A reminder that when we update the fields programmatically, the `'change'` event is NOT triggered, so we finally have to ensure we call `updatePoints` to re-create the points again over the image container.
- You can now validate this by actually doing drag & drop and checking things get updated correctly in the UI, save the values and check the front-facing page.

```js
class SchematicEditHandler extends Controller {
    // ... targets

    connect() {
      this.setupImageInputObserver();
      this.setupImageDropHandlers();
      this.updatePoints();
    }

    /**
     * Once a new point target (for each point within the inline panel) is connected
     * add an event listener to the delete button so we know when to re-update the points.
     *
     * @param {HTMLElement} element
     */
    pointTargetConnected(element) {
      const deletePointButton = element
        .closest("[data-inline-panel-child]")
        .querySelector('[id*="DELETE-button"]');

      deletePointButton.addEventListener("click", (event) => {
        this.updatePoints(event);
      });
    }

    /**
     * Allow the point to be dragged using the 'move' effect and set its data.
     *
     * @param {DragEvent} event
     */
    pointDragStart(event) {
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.setData("text/plain", event.target.dataset.id);
      event.target.style.opacity = "0.5";
    }

    /**
     * When dragging finishes on a point, reset its opacity.
     *
     * @param {DragEvent} event
     */
    pointDragEnd({ target }) {
      target.style.opacity = "1";
    }

    // setupImageInputObserver() { ...


    /**
     * Once connected, set up the dragover and drop events on the preview image container.
     * We are unable to easily do this with `data-action` attributes in the template.
     */
    setupImageDropHandlers() {
      const previewImageContainer = this.imageInputTarget
        .closest(".field-content")
        .querySelector(".preview-image");

      previewImageContainer.addEventListener("dragover", (event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = "move";
      });

      previewImageContainer.addEventListener("drop", (event) => {
        event.preventDefault();

        const inputId = event.dataTransfer.getData("text/plain");
        const { height, width } = previewImageContainer.getBoundingClientRect();

        const xNumber = event.offsetX / width + Number.EPSILON;
        const x = Math.round(xNumber * 10000) / 100;
        const yNumber = 1 - event.offsetY / height + Number.EPSILON;
        const y = Math.round(yNumber * 10000) / 100;

        const inlinePanel = document
          .getElementById(inputId)
          .closest("[data-inline-panel-child]");

        inlinePanel.querySelector("[data-point-x]").value = x;
        inlinePanel.querySelector("[data-point-y]").value = y;

        this.updatePoints(event);
      });
    }

    // updateImage(newValue) { ... etc & rest of controller

```

## Finishing Up & Next Steps

- You should now have a functional user interface where we can build a schematic snippet with points visually shown over the image in the editor and in the front-facing page that uses it.
- We should be able to update the points via their fields and if you did step 6, via drag and drop on the actual points within the editor.
- I would love to hear your **feedback** on this post, let me know what issues you encountered or where you could see improvements.
- If you liked this, please **add a comment or reaction** to the post or even [**shout me a coffee**](https://www.buymeacoffee.com/lb.ee).
- You can see the full working code, broken up into discrete commits, on my [schematic-builder tutorial branch](https://github.com/lb-/bakerydemo/commits/tutorial/schematic-builder).

### Further Improvements

Here are some ideas for improvements you can give a go at yourself.

- Add colours for points to align with the colours in the inline panels so that the point/field mapping can be easier to work with.
- Add better keyboard control, focusable elements and up/down/left/right 'nudging', a lot of this can be done via adding more `data-action` attributes on the point `template` and working from there.
- Add better handling of drag/drop on mobile devices, the HTML5 Drag & Drop API does not support mobile devices great, maybe an external library would be good to explore.

### Why Stimulus and not ... other things

I originally built this in late 2021 when doing some consulting, at the time I called the model `Diagram` but `Schematic` sounded better.

The [original implementation was done in jQuery](https://gist.github.com/lb-/55fea7ec9a0be6b6c2d9184a9d77f711) and adding all the event listeners to the `InlinePanel` ended up being quite a mess, I could not get a bunch of the functionality to work well that is in this final tutorial and the parts of the JS/HTML were all over the place so it would have been hard to maintain.

Since then, I have been investigating some options for a lightweight JS framework in the Wagtail core codebase. Stimulus kept popping up in discussions but I initially wrote it off and was expecting Alpine.js to be a solid candidate. However, Alpine.js has a much larger API and also has a large CSP compliance risk that pretty much writes it off (yes, the docs say they have a CSP version but as of writing that is not actually released or working, also it pretty much negates all the benefits of Alpine).

After doing some small things with Stimulus, I thought this code I had written would be a good example of a semi-larger thing that needs to interact with existing DOM and dynamic DOM elements without having to dig into the other JS used by the `InlinePanel` code.

I do not know where the Wagtail decision will head, you can read more of the [UI Technical Debt discussion](https://github.com/wagtail/wagtail/discussions/7689#discussioncomment-2037913) if you want. However, for lightweight JS interaction where you do not have, or need to have, full control over the entire DOM Stimulus appears to be a really solid choice without getting in the way and letting you work in 'vanilla' JS for all the real work and helps you with the common things like targeting elements/initialising JS behaviour and managing event listeners.

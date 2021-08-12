# Guide app

## Goal

* Create a simple way for contextual help to be shown to CMS users while using Wagtail, that can be maintained within the Wagtail admin UI itself.

## Overview
* Each `guide` will be able to be mapped to a page within the admin.
* Each `guide` will be able to have one or more steps with basic text content and the option to align a step with a UI element.
* If a guide is available for the current page it will be highlighted in the menu. If no guide is available for the current page the menu will simply load a listing of all guides.

## Implementation Overview

* Wagtail `modelAdmin` and `hooks` will be used to add the customisation.
* Shepherd.js will be used to present the UI steps in an interactive way, this is a great JS library that allows a series of 'steps' to be declared that take the user through a tour as a series of popovers, some steps can be aligned to an element in the UI and that element will be highlighted.

### Versions

* Django 3.2
* Wagtail 2.14
* Shepherd.js 8.3.1 


## Tutorial


### 1. Create the guide app

* Use the Django [`startapp`](https://docs.djangoproject.com/en/3.2/ref/django-admin/#startapp) command to create a new app `'guide'` which will contain all the new models and code for this feature.
* `./manage.py startapp guide`
* Update the settings `INSTALLED_APPS` with the new `guide` app created
* Run the initial migration `./manage.py makemigrations guide`

### 2. Create the models

* We will create two new models; `Guide` and `GuideStep`.
* Where `Guide` contains a title (for searching), a url path (to determine what admin UI page it should be shown on) and links to one or more steps. We want to provide the user a way to order the steps, even re-order them later.
* Where `GuideStep` contains a title, text and a potential element selector. The data needed is based on the options that can be passed to the [Shepherd.js `step`s](https://shepherdjs.dev/docs/Step.html).
* This code is based on the [Inline Panels and Model Clusters](https://docs.wagtail.io/en/stable/reference/pages/panels.html#inline-panels) instructions in the Wagtail docs.
* After creating the models, remember to run migrations & migrate `/manage.py makemigrations` & `/manage.py migrate`.

```python
# guide/models.py

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel


class GuideStep(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    element = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
        FieldPanel('element'),
    ]

    class Meta:
        abstract = True

class GuideRelatedStep(Orderable, GuideStep):
    guide = ParentalKey('guide.Guide', on_delete=models.CASCADE, related_name='steps')


class Guide(ClusterableModel):
    title = models.CharField(max_length=255)
    # steps - see GuideRelatedStep
    url_path = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        InlinePanel('steps', label="Steps", min_num=1),
        FieldPanel('url_path'),
    ]
```

### 3. Add the hooks for the `modelAdmin`

* Using the `modelAdmin` system we will create a a basic admin module for our `Guide` model, this code is based on the [modelAdmin example in the docs](https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/index.html#a-simple-example).
* Note that we have turned ON `inspect_view_enabled`, this is so that a read only view of each guide is available and it also ensures that non-editors of this model can be given access to this data, these permissions are checked for showing the menu item also.
* Using `modelAdmin` will set up a new menu item in the sidebar.
* Use jsdelivr to add global JS for the Shepherd.js library, we will need this in the next few steps. This has been added using the `hooks` system and the hook [`insert_global_admin_js`](https://docs.wagtail.io/en/stable/reference/hooks.html#insert-global-admin-js).
* Remember to give all users permission to 'inspect' Guides (otherwise the menu will not show)


```python
# guide/wagtail_hooks.py
from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import Guide

class GuideAdmin(ModelAdmin):
    menu_label = 'Help'
    model = Guide
    menu_icon = 'help'
    menu_order = 8000
    list_display = ('title', 'url_path')
    search_fields = ('title', 'url_path')
    inspect_view_enabled = True


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        'https://cdn.jsdelivr.net/npm/shepherd.js@8/dist/js/shepherd.min.js'
    )


modeladmin_register(GuideAdmin)
```

### 4. Add styles for Shepherd.js

* We will need to also import the css for the Shepherd.js library, however if we use the hook `insert_global_admin_css`, then this css will come after the Wagtail styles, which actually makes it harder to style so we will instead override the base admin template.
* This can be done by [customising admin templates](https://docs.wagtail.io/en/stable/advanced_topics/customisation/admin_templates.html), once the Wagtail admin app is installed, we can add a file that will replace the existing template.
* `guide/templates/wagtailadmin/admin_base.html` is the file path (note: it can also be put at the root templates folder) and we will extend the existing admin template but with a css import added.


```html
{% extends "wagtailadmin/admin_base.html" %}

{% block css %}
    {# extend the admin_base template so that shepherd styles can be first and Wagtail styles will override #}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/shepherd.js@8/dist/css/shepherd.css">
    {{ block.super }}
{% endblock %}
```

### 5. Add a custom MenuItem

* The next step is to customise the `MenuItem` in the sidebar menu with our own, this will do the work of determining if the current page has a `Guide` available and passing data to the template which will be used by Shephard.js
* `GuideAdminMenuItem` will be a new class that will override the `get_context` method.
* `path_to_match = re.sub('[\d]+', '#', request.path)` will take the current request path (e.g. `/admin/images/53/`) and convert it to one where any numbers are replaced with a hash (e.g. `/admin/images/#/`), this is a simple way to allow fuzzy URL matching.
* The rest of the method is updating classes and passing data for the steps.
* We then need to use this `GuideAdminMenuItem` in the `GuideAdmin` by overriding the `get_menu_item` method.
* You should now be able to create a new `Guide` from the sidebar menu and if you put the url_path in as `/admin/` and go to the Dashboard (home) page in the admin there will be an id of 'start-tour' on the Menu item.
* Remember to `return context`, otherwise you will just get a blank menu item.

```python
# guide/menu.py
import re

from django.utils.safestring import mark_safe

from wagtail.contrib.modeladmin.menus import ModelAdminMenuItem

from .models import Guide


class GuideAdminMenuItem(ModelAdminMenuItem):

    def get_context(self, request):
        context = super().get_context(request)
        # allow for a simple approach to fuzzy matching, any paths with numbers will be replaced with '#'
        path_to_match = re.sub('[\d]+', '#', request.path)
        guide = Guide.objects.filter(url_path=path_to_match).first()

        if guide:
            context['attr_string'] = context['attr_string'] + ' ' + mark_safe('id=start-tour')
            context['classnames'] = context['classnames'] + ' help-available'

            steps = [
                {
                    'title': step.title,
                    'text': step.text,
                    'element': step.element
                } for step in guide.steps.all()
            ]

            context['guide_options'] = {'steps': steps}

        return context
```

```python
# guide/wagtail_hooks.py
# ... other imports

from .menu import GuideAdminMenuItem


class GuideAdmin(ModelAdmin):
    #...rest of ModelAdmin (inspect_view_enabled etc)

    def get_menu_item(self, order=None):
        return GuideAdminMenuItem(self, order or self.get_menu_order())

```

### 6. Add the JS via a new menu item template

* There is a fair bit to unpack in this final step, but the goal is to provide the right `options` to the Shepherd.js library and when the user clicks the menu item button, instead of going to the Guide listing it should trigger the tour.
* In this new template `guide/templates/guide/menu_item.html` we will have the following;
  * `{% load wagtailadmin_tags %}` - loading tags
  * `{{ guide_options|json_script:"guide-options" }}` - leveraging the Django [`json_script`](https://docs.djangoproject.com/en/3.2/ref/templates/builtins/#json-script) filter which will safely convert the `guide_options` from context into JSON to be used by our JS code.
  * `<li ...` - this is a copy of the existing Wagtail template at `wagtail/admin/templates/wagtailadmin/shared/menu_item.html`
  * `<style>...` - adding some basic styling of the menu item when there is a known guide to show
  * `<script>` - let's break this down below
* `const { steps = [] } = JSON.parse` will pull out the `steps` from the JSON data set up by `json_script`
* `options` - building up the options data to pass into the `Shepherd.Tour` class with some reasonable defaults and each step configured, including some behaviour so that there is no 'back' button if only one step exists and there is a 'Finished' button on the last step.
* `window.addEventListener('DOMContentLoaded` - when the DOM is loaded we want to create the `tour` based on the `options`, with some additional defaults for `buttons` (showing a back & next) button for all items.
* We then find the `start-tour` id and, if present, attach an `onClick` listener to it which will start the Tour.
* The last step at the end of this section is to update the `GuideAdminMenuItem` `template` to refer to this template file.
* Note that there are more 'clean' ways to achieve this set up, adding the JS/Styles inline within this template is not ideal, however for the sake of this tutorial it will work well enough and can be optimised later.


```html
{# guide/templates/guide/menu_item.html #}
{% load wagtailadmin_tags %}

{{ guide_options|json_script:"guide-options" }}

<li class="menu-item{% if active %} menu-active{% endif %}">
    <a href="{{ url }}"
       class="{{ classnames }}"
       {{ attr_string }}>
        {% if icon_name %}{% icon icon_name 'icon--menuitem' %}{% endif %}
        {{ label }}
    </a>
</li>

<style>
  .menu-item .help-available::after {
    content: '*';
  }
</style>

<script>
  const { steps = [] } = JSON.parse(document.getElementById('guide-options').textContent);

  const options = {
    defaultStepOptions: {
      arrow: false,
      cancelIcon: { enabled: true },
      canClickTarget: false,
      classes: '',
      scrollTo: { behavior: 'smooth', block: 'center' },
    },
    steps: steps.map(({ element, ...step }, index) => ({
      ...step,
      ...(element ? { attachTo: { element } } : {}),
      ...(index === steps.length - 1 ? {
        buttons: [
          ...(steps.length === 1 ? [] : [
            {
              action() { return this.back(); },
              classes: 'button button-small button-secondary',
              secondary: true,
              text: 'Back'
            },
          ]),
          {
            action() { return this.next(); },
            classes: 'button button-small',
            text: 'Finished'
          }
        ]
      } : {})
    })),
    useModalOverlay: true,
  };


  window.addEventListener('DOMContentLoaded', () => {
    const tour = new Shepherd.Tour({
      ...options, defaultStepOptions: {
        ...options.defaultStepOptions, buttons: [
          {
            action() {
              return this.back();
            },
            classes: 'button button-small button-secondary',
            secondary: true,
            text: 'Back'
          },
          {
            action() {
              return this.next();
            },
            classes: 'button button-small',
            text: 'Next'
          }
        ]
      }
    });

    const link = document.getElementById('start-tour');

    link && link.addEventListener('click', (event) => {
      event.preventDefault();
      tour.start();
    });
  });
</script>
```

```python

class GuideAdminMenuItem(ModelAdminMenuItem):
    template = 'guide/menu_item.html'

    # ...
```

## Final Implementation

Now that this has been implemented, Admins should be able to create a new Guide via the sidebar menu like below.


This should create a variant of the Guide menu on the dashboard page, that, when clicked will activate the guide for that page.


## Future Enhancements

* Having the same Menu Item trigger the guide AND show the guide listing is not ideal, as this could be confusing for users, plus it might be confusing to admins when they actually want to edit and cannot easily get to the guide listing (if there are lots of guides added).
* Make a dashboard panel available to new users if there is a matching guide available for that page.
* Make the inspect view for Guide items show the full steps, as this will be a helpful resource.
* Have a way to track what users click on what guides, especially helpful for new users, maybe even provide feedback.
* Add a core Guide settings model, available in the settings menu, that will provide a way to show content to the help listing and other useful settings.
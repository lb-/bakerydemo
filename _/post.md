Title: Image Uploads in Wagtail Forms

By-line: For developers using the Wagtail CMS who want to add image upload fields.

Heads up - This is an update of my earlier post [Image Uploads in Wagtail Forms](https://posts-by.lb.ee/image-uploads-in-wagtail-forms-3121c9b35d27) which was written for Wagtail v1.12, this new post is written for v2.10/v2.11.

**The Problem** --- Your team are loving the custom form builder in Wagtail CMS and want to let people upload an image along with the form.

**The Solution** --- Define a new form field type that is selectable when editing fields in the CMS Admin, this field type will be called 'Upload Image'. This field should show up in the view as a normal upload field with restrictions on file type and size, just like the Wagtail Images system.

**IMAGE 1 - CMS field type available**

Note the Field Type: 'Upload Image' --- that is what we want to build.

**IMAGE 3 - form view with field**

Goal: When you add an 'Upload Image' field, it will show up on the form view for you.

Wagtail, Images and Forms
=========================

Skip ahead if you know the basics here.

[Wagtail](https://wagtail.io/) is a Content Management System (CMS) that is built on top of the [Django Web Framework](https://www.djangoproject.com/). What I love about Wagtail is that it embraces the Django ecosystem and way of doing things. It also has a really nice admin interface that makes it easy for users to interact with the content.

Wagtail has a built in interface and framework for uploading, storing and serving images. This is aptly named Wagtail Images, you can review the docs about [Using Images in Templates](https://docs.wagtail.io/en/v2.10.1/topics/images.html) or [Advanced Image Usage](https://docs.wagtail.io/en/v2.10.1/advanced_topics/images/index.html) for more information.

Wagtail comes with a great [Form Builder](https://docs.wagtail.io/en/v2.10.1/reference/contrib/forms/index.html) module, it lets users build their own forms in the admin interface. These forms can have a series of fields such as Text, Multi-line Text, Email, URL, Checkbox, and others that build up a form page that can be viewed on the front end of the website. Users can customise the default value, whether the field is required and also some help text that relates to the field.

Before We Start
===============

Before we start changing (breaking) things, it is important that you have the following items completed.

1. Wagtail v2.10.x or v2.11.x up and running as per the [main documentation](https://docs.wagtail.io/en/v2.10.1/).
2. [Wagtailforms module](https://docs.wagtail.io/en/v2.10.1/reference/contrib/forms/index.html#usage) is installed, running and you have forms working.

Adding Image Upload Fields to Forms in Wagtail
==============================================

Planning our Changes
--------------------

We want to enable the following user interaction:

1. The admin interface should provide the ability to edit an existing form and create a new form as normal.
2. When editing a form page, there should be a new dropdown option on the 'Field Type' field called 'Upload Image'.
3. The form page view should have one file upload field for every 'Upload Image' field that was defined in the admin.
4. The form page view should accept images with the same restrictions as Wagtail Images (< 10mb, only PNG/JPG/GIF*).
5. The form page view should require the image if the field is defined as 'required' in admin.
6. When an image is valid, it should save this image into the Wagtail Images area.
7. A link to the image should be saved to the form submission (aka form response), this will ensure it appears on emails or reports.

* \* Default GIF support is quite basic in Wagtail, if you want to support animated GIFs you should read these docs regarding [Animated GIFs](https://docs.wagtail.io/en/v2.10.1/advanced_topics/images/animated_gifs.html).

1\. Extend the `AbstractFormField` Class
----------------------------------------

In your models file that contains your `FormPage` class definition, you should also have a definition for a `FormField` class. In the original definition, the [AbstractFormField class](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/contrib/forms/models.py#L80) uses a fixed tuple of [FORM_FIELD_CHOICES](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/contrib/forms/models.py#L24). We need to override the field_type with an appended set of choices.

```python
# models.py

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, FORM_FIELD_CHOICES

class FormField(AbstractFormField):

    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=list(FORM_FIELD_CHOICES) + [('image', 'Upload Image')]
    )

    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)

```

In the above code you can see that we imported the original `FORM_FIELD_CHOICES` from wagtail.contrib.forms.models. We then converted it to a list, added our new field type and then this is used in the choices argument of the `field_type` field.

When you do this, you will need to [make a migration, and run that migration](https://docs.djangoproject.com/en/3.1/ref/django-admin/#django-admin-makemigrations). Test it out, the form in admin will now let you select this type, but it will not do much else yet.

2\. Extend the `FormBuilder` Class
----------------------------------

In your models file you will now need to create an extended form builder class. In the original definition the [FormBuilder class](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/contrib/forms/forms.py#L22) builds a form based on the `field_type` list that is stored in each FormPage instance. We can follow the example in the docs about [Adding a custom field type](https://docs.wagtail.io/en/v2.10.1/reference/contrib/forms/customisation.html#adding-a-custom-field-type).

We will need to create a method that follows the convention based on the field name ('image' in our case) to a method name `create_image_field` which is then called and should return an instance of a [Django form widget](https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#widget). Rather than building our own custom Image field that works with Wagtail, we can use their own [WagtailImageField](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/images/fields.py#L14).

```python
# models.py

from wagtail.contrib.forms.forms import FormBuilder

from wagtail.images.fields import WagtailImageField


class CustomFormBuilder(FormBuilder):

    def create_image_field(self, field, options):
        return WagtailImageField(**options)

```

In the above code, we have imported `FormBuilder` from `wagtail.contrib.forms.forms` and `WagtailImageField` from `wagtail.images.fields`, then created our own custom `FormBuilder` with a new class. We have added a method `create_date_field` that returns a created `WagtailImageField`, passing in any options provided.

3\. Set the FormPage class to use CustomFormBuilder
---------------------------------------------------

This step is pretty straight forward, we want to override the `form_builder` definition in our FormPage model. This is a very nifty way that Wagtail enables you to override the form_builder you use.

```python
# models.py

from wagtail.contrib.forms.models import AbstractForm

class FormPage(AbstractForm):

    form_builder = CustomFormBuilder

    #... rest of the FormPage definition

```

**IMAGE 1 - able to select field**

4\. Update form page template to accept File Data
-------------------------------------------------

The form page view should have a `<form />` tag in it, the implementation suggested by Wagtail does not allow files data to be submitted in the form.

```html
<!-- templates/form_page.html -->

{% extends "base.html" %}

{% load wagtailcore_tags %}

{% block content %}

    {{ self.intro }}

    <form action="{% pageurl self %}" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" />
    </form>

{% endblock %}
```

The only difference to the basic form is that we have added `enctype="multipart/form-data"` to our form attributes. **If you do not do this you will never get any files sent through the request and no errors to advise you why**.

For more information about why we need to do this, you can view the [Django Docs File Uploads](https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/#basic-file-uploads) page and have a deep dive into the [enctype form attribute on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#attr-enctype).

5\. Add ability to edit which collection images will be added to
----------------------------------------------------------------

When uploading images via the admin interface, there is an option to add each image to a collection, this defaults to 'Root' and these act like folders for your images.

Rather than just dumping all uploaded images from form submissions into 'Root' we want to give the user the option to determine which `Collection` the images for each page form will be added to.

```python
# models.py

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Collection


class FormPage(AbstractForm):

    form_builder = CustomFormBuilder

    # other fields...

    uploaded_image_collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # content_panels...

    settings_panels = AbstractForm.settings_panels + [
        FieldPanel('uploaded_image_collection')
    ]


    def get_uploaded_image_collection(self):
        """
        Returns a Wagtail Collection, using this form's saved value if present,
        otherwise returns the 'Root' Collection.
        """
        collection = self.uploaded_image_collection
        return collection or Collection.get_first_root_node()

```

In the code above we import the `Collections` model, added a new field to our `FormPage` model called `uploaded_image_collection` which is a [ForeignKey relation](https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey) to the `'wagtailCore.Collection'` model.

We also added a class method to retrieve this from the Page and fall back to the root collection via the [get_first_root_node](https://django-treebeard.readthedocs.io/en/latest/api.html?#treebeard.models.Node.get_first_root_node) method (as Wagtail Collections use Treebeard to define a tree like structure).

Once this code step is completed, you will need to [make a migration, and run that migration](https://docs.djangoproject.com/en/3.1/ref/django-admin/#django-admin-makemigrations).

**IMAGE 2 - selecting image collection**

6\. Process the Image (file) Data after Validation
--------------------------------------------------

We will now override the `process_form_submission` on our FormPage class. The original definition of the [process_form_submission method](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/contrib/forms/models.py#L260) has no notion of processing anything other than the `request.POST` data. It will simply convert the cleaned data to JSON for storing on the form submission instance. We will iterate through each field and find any instances of WagtailImageField then get the data, create a new Wagtail Image with that file data, finally we will store a link to the image in the response.

```python
# models.py

import json
from os.path import splitext

from django.core.serializers.json import DjangoJSONEncoder

from wagtail.images import get_image_model


class FormPage(AbstractForm):

    form_builder = CustomFormBuilder

    # fields & panels definitions...

    @staticmethod
    def get_image_title(filename):
        """
        Generates a usable title from the filename of an image upload.
        Note: The filename will be provided as a 'path/to/file.jpg'
        """

        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()
        return ''

    def process_form_submission(self, form):
        """
        Processes the form submission, if an Image upload is found, pull out the
        files data, create an actual Wgtail Image and reference its ID only in the
        stored form response.
        """

        cleaned_data = form.cleaned_data

        for name, field in form.fields.items():
            if isinstance(field, WagtailImageField):
                image_file_data = cleaned_data[name]
                if image_file_data:
                    ImageModel = get_image_model()

                    kwargs = {
                        'file': cleaned_data[name],
                        'title': self.get_image_title(cleaned_data[name].name),
                        'collection': self.get_uploaded_image_collection(),
                    }

                    if form.user and not form.user.is_anonymous:
                        kwargs['uploaded_by_user'] = form.user

                    image = ImageModel(**kwargs)
                    image.save()
                    # saving the image id
                    # alternatively we can store a path to the image via image.get_rendition
                    cleaned_data.update({name: image.pk})
                else:
                    # remove the value from the data
                    del cleaned_data[name]

        submission = self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
        )

        # important: if extending AbstractEmailForm, email logic must be re-added here
        # if self.to_address:
        #    self.send_mail(form)

        return submission
```

Once this is applied, you should be able to submit a form response with an uploaded image.

**IMAGE 3 - form view with field**

A few items of note here:

* Using [`get_image_model`](https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html#module-wagtail.images) is the best practice way to get the Image Model that Wagtail is using.
* `cleaned_data` contains the File Data (for any files), the Django form module does this for us. File Data cannot be parsed by the JSON parser, hence us having to process into a URL or Image ID for these cases.
* The staticmethod `get_image_title` can look like whatever you want, I stripped out dashes and made the file title case. You do not have to do this but you do have to ensure there is some title when inserting a `WagtailImage`.
* If our FormPage is actually extending `AbstractEmailForm` (ie. the form submits AND sends an email) we must ensure that the [send_mail code](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/contrib/forms/models.py#L342) is added.
* You must use `cleaned_data.update` to save a JSON seralizable reference to your image, hence the file data will not work.

7\. Viewing the image via the form submissions listing
------------------------------------------------------

The final step is to provide a way for this image to be easily viewed in the submission listing view, we can do this by [customising how this list generates](https://docs.wagtail.io/en/v2.10.1/reference/contrib/forms/customisation.html#customise-form-submissions-listing-in-wagtail-admin).

We have stored an id of the image but we want to use `image.get_rendition`, which is a very useful function detailed in the [Wagtail Documentation](https://docs.wagtail.io/en/v2.10.1/advanced_topics/images/renditions.html). This function mimics the template helper but can be used in Python. By default the URL will be relative (it will not contain the http/https, or the domain), this will mean links sent to email will not work. It is up to you to work out how to best solve this if it is an issue.

```python
# models.py

from django.utils.html import format_html
from django.urls import reverse

from wagtail.contrib.forms.views import SubmissionsListView


class CustomSubmissionsListView(SubmissionsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # generate a list of field types, the first being the injected 'submission date'
        field_types = ['submission_date'] + [field.field_type for field in self.form_page.get_form_fields()]
        data_rows = context['data_rows']

        if not self.is_export:
            ImageModel = get_image_model()

            for data_row in data_rows:

                fields = data_row['fields']

                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    if field_type == 'image' and value:
                        image = ImageModel.objects.get(pk=value)
                        rendition = image.get_rendition('fill-100x75|jpegquality-40')
                        preview_url = rendition.url
                        url = reverse('wagtailimages:edit', args=(image.id,))
                        # build up a link to the image, using the image title & id
                        fields[idx] = format_html(
                            "<a href='{}'><img alt='Uploaded image - {}' src='{}' />{} ({})</a>",
                            url,
                            image.title,
                            preview_url,
                            image.title,
                            value
                        )

        return context

class FormPage(AbstractForm):

    form_builder = CustomFormBuilder
    submissions_list_view_class = CustomSubmissionsListView # added

```

In the code above we have added a new CustomSubmissionsListView that extends the Wagtail SubmissionsListView which will have a custom get_context_data method. In this method we call the original [get_context_data](https://github.com/wagtail/wagtail/blob/v2.10.1/wagtail/contrib/forms/views.py#L249) to get the generated context data.

Then we check if we are showing the submissions to the user (instead of exporting them) and map through each submission row, checking with values are images and updating the shown value with some HTML. This HTML will contain a preview of the image (using rendition) with some description based on the title and id within a link to the admin page for that image.

**IMAGE 4 - Submission Listing**

Finishing Up
============

Your Form models.py file will now look something like the following:

```python
# models.py

import json
from os.path import splitext

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.html import format_html
from django.urls import reverse

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.models import Collection
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField, FORM_FIELD_CHOICES
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.images import get_image_model
from wagtail.images.fields import WagtailImageField


class CustomFormBuilder(FormBuilder):

    def create_image_field(self, field, options):
        return WagtailImageField(**options)


class CustomSubmissionsListView(SubmissionsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # generate a list of field types, the first being the injected 'submission date'
        field_types = ['submission_date'] + [field.field_type for field in self.form_page.get_form_fields()]
        data_rows = context['data_rows']

        if not self.is_export:
            ImageModel = get_image_model()

            for data_row in data_rows:

                fields = data_row['fields']

                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    if field_type == 'image' and value:
                        image = ImageModel.objects.get(pk=value)
                        rendition = image.get_rendition('fill-100x75|jpegquality-40')
                        preview_url = rendition.url
                        url = reverse('wagtailimages:edit', args=(image.id,))
                        # build up a link to the image, using the image title & id
                        fields[idx] = format_html(
                            "<a href='{}'><img alt='Uploaded image - {}' src='{}' />{} ({})</a>",
                            url,
                            image.title,
                            preview_url,
                            image.title,
                            value
                        )

        return context


class FormField(AbstractFormField):

    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=list(FORM_FIELD_CHOICES) + [('image', 'Upload Image')]
    )

    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(AbstractForm):

    form_builder = CustomFormBuilder
    submissions_list_view_class = CustomSubmissionsListView

    # ... fields

    uploaded_image_collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    content_panels = AbstractForm.content_panels + [
        # ... panels
    ]

    settings_panels = AbstractForm.settings_panels + [
        FieldPanel('uploaded_image_collection')
    ]

    def get_uploaded_image_collection(self):
        """
        Returns a Wagtail Collection, using this form's saved value if present,
        otherwise returns the 'Root' Collection.
        """
        collection = self.uploaded_image_collection

        return collection or Collection.get_first_root_node()

    @staticmethod
    def get_image_title(filename):
        """
        Generates a usable title from the filename of an image upload.
        Note: The filename will be provided as a 'path/to/file.jpg'
        """

        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()
        return ''

    def process_form_submission(self, form):
        """
        Processes the form submission, if an Image upload is found, pull out the
        files data, create an actual Wgtail Image and reference its ID only in the
        stored form response.
        """

        cleaned_data = form.cleaned_data

        for name, field in form.fields.items():
            if isinstance(field, WagtailImageField):
                image_file_data = cleaned_data[name]
                if image_file_data:
                    ImageModel = get_image_model()

                    kwargs = {
                        'file': cleaned_data[name],
                        'title': self.get_image_title(cleaned_data[name].name),
                        'collection': self.get_uploaded_image_collection(),
                    }

                    if form.user and not form.user.is_anonymous:
                        kwargs['uploaded_by_user'] = form.user

                    image = ImageModel(**kwargs)
                    image.save()
                    # saving the image id
                    # alternatively we can store a path to the image via image.get_rendition
                    cleaned_data.update({name: image.pk})
                else:
                    # remove the value from the data
                    del cleaned_data[name]

        submission = self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
        )

        # important: if extending AbstractEmailForm, email logic must be re-added here
        # if self.to_address:
        #    self.send_mail(form)

        return submission

```

Forms can now have one or more Image Upload fields that are defined by the CMS editors. These images will be available in Admin in the Images section and can be used throughout the rest of Wagtail. You also get all the benefits that come with Wagtail Images like search indexing, usage in templates and URLS for images of various compressed sizes.

**IMAGE 3 - form view with field**

The Admin view of form responses will now show whatever you store from the `clean_data`.

Let me know if you run into issues or find some typos/bugs in this article. Thank you to the amazing team at Torchbox and all the developers of Wagtail for making this amazing tool. Show your support of Wagtail by starring the [Wagtail repo on Github](https://github.com/wagtail/wagtail/).

Thanks to my friend Adam for helping me proof this.

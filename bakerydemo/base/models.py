import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django import forms

from modelcluster.fields import ParentalKey

from wagtail.contrib.forms.models import (
    AbstractEmailForm, AbstractFormField, AbstractFormSubmission, FORM_FIELD_CHOICES)
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.views import SubmissionsListView


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=FORM_FIELD_CHOICES + (('fileupload', 'File Upload'),)
    )


class CustomFormBuilder(FormBuilder):

    def create_fileupload_field(self, field, options):
        return forms.FileField(**options)


class CustomSubmissionsListView(SubmissionsListView):
    """
    further customisation of submission list can be done here
    """
    pass


class CustomFormSubmission(AbstractFormSubmission):
    # important - adding this custom model will make existing submissions unavailable
    # can be resolved with a custom migration

    def get_data(self):
        """
        Here we hook in to the data representation that the form submission returns
        Note: there is another way to do this with a custom SubmissionsListView
        However, this gives a bit more granular control
        """

        file_form_fields = [
            field.clean_name for field in self.page.specific.get_form_fields()
            if field.field_type == 'fileupload'
        ]

        data = super().get_data()

        for field_name, field_vale in data.items():
            if field_name in file_form_fields:
                # now we can update the 'representation' of this value
                # we could query the FormUploadedFile based on field_vale (pk)
                # then return the filename etc.
                pass

        return data


class FormUploadedFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    field_name = models.CharField(blank=True, max_length=254)


class FormPage(AbstractEmailForm):

    form_builder = CustomFormBuilder
    submissions_list_view_class = CustomSubmissionsListView

    # ... other fields (image, body etc)

    content_panels = AbstractEmailForm.content_panels + [
        # ...
    ]

    def get_submission_class(self):
        """
        Returns submission class.
        Important: will make your existing data no longer visible, only needed if you want to customise
        the get_data call on the form submission class, but might come in handy if you do it early

        You can override this method to provide custom submission class.
        Your class must be inherited from AbstractFormSubmission.
        """

        return CustomFormSubmission

    def process_form_submission(self, form):
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.

        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
        """

        file_form_fields = [field.clean_name for field in self.get_form_fields() if field.field_type == 'fileupload']

        for (field_name, field_value) in form.cleaned_data.items():
            if field_name in file_form_fields:
                uploaded_file = FormUploadedFile.objects.create(
                    file=field_value,
                    field_name=field_name
                )

                # store a reference to the pk (as this can be converted to JSON)
                form.cleaned_data[field_name] = uploaded_file.pk

        return self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
        )

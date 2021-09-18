from __future__ import unicode_literals

from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
    widget_with_script,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    FORM_FIELD_CHOICES,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .blocks import BaseStreamBlock


@register_snippet
class People(index.Indexed, ClusterableModel):
    """
    A Django model to store People objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/base/people/)

    `People` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name", classname="col6"),
                        FieldPanel("last_name", classname="col6"),
                    ]
                )
            ],
            "Name",
        ),
        FieldPanel("job_title"),
        ImageChooserPanel("image"),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ""

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """

    body = RichTextField()

    panels = [
        FieldPanel("body"),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = "Footer Text"


class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    body = StreamField(BaseStreamBlock(), verbose_name="Page body", blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        StreamFieldPanel("body"),
        ImageChooserPanel("image"),
    ]


class HomePage(Page):
    """
    The Home Page. This looks slightly more complicated than it is. You can
    see if you visit your site and edit the homepage that it is split between
    a:
    - Hero area
    - Body area
    - A promotional area
    - Moveable featured site sections
    """

    # Hero section of HomePage
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(
        max_length=255, help_text="Write an introduction for the bakery"
    )
    hero_cta = models.CharField(
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    # Body section of the HomePage
    body = StreamField(BaseStreamBlock(), verbose_name="Home content block", blank=True)

    # Promo section of the HomePage
    promo_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Promo image",
    )
    promo_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Title to display above the promo copy",
    )
    promo_text = RichTextField(
        null=True, blank=True, help_text="Write some promotional copy"
    )

    # Featured sections on the HomePage
    # You will see on templates/base/home_page.html that these are treated
    # in different ways, and displayed in different areas of the page.
    # Each list their children items that we access via the children function
    # that we define on the individual Page models e.g. BlogIndexPage
    featured_section_1_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Title to display above the promo copy",
    )
    featured_section_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="First featured section for the homepage. Will display up to "
        "three child items.",
        verbose_name="Featured section 1",
    )

    featured_section_2_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Title to display above the promo copy",
    )
    featured_section_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Second featured section for the homepage. Will display up to "
        "three child items.",
        verbose_name="Featured section 2",
    )

    featured_section_3_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Title to display above the promo copy",
    )
    featured_section_3 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Third featured section for the homepage. Will display up to "
        "six child items.",
        verbose_name="Featured section 3",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                FieldPanel("hero_text", classname="full"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta"),
                        PageChooserPanel("hero_cta_link"),
                    ]
                ),
            ],
            heading="Hero section",
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("promo_image"),
                FieldPanel("promo_title"),
                FieldPanel("promo_text"),
            ],
            heading="Promo section",
        ),
        StreamFieldPanel("body"),
        MultiFieldPanel(
            [
                MultiFieldPanel(
                    [
                        FieldPanel("featured_section_1_title"),
                        PageChooserPanel("featured_section_1"),
                    ]
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("featured_section_2_title"),
                        PageChooserPanel("featured_section_2"),
                    ]
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("featured_section_3_title"),
                        PageChooserPanel("featured_section_3"),
                    ]
                ),
            ],
            heading="Featured homepage sections",
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.title


class GalleryPage(Page):
    """
    This is a page to list locations from the selected Collection. We use a Q
    object to list any Collection created (/admin/collections/) even if they
    contain no items. In this demo we use it for a GalleryPage,
    and is intended to show the extensibility of this aspect of Wagtail
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    )
    body = StreamField(BaseStreamBlock(), verbose_name="Page body", blank=True)
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select the image collection for this gallery.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        StreamFieldPanel("body"),
        ImageChooserPanel("image"),
        FieldPanel("collection"),
    ]

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    subpage_types = []


class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    http://docs.wagtail.io/en/latest/reference/contrib/forms/index.html
    """

    # https://docs.wagtail.io/en/stable/reference/contrib/forms/customisation.html#adding-a-custom-field-type

    CHOICES = FORM_FIELD_CHOICES + (("section", "Section"),)

    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)

    field_type = models.CharField(
        verbose_name="field type", max_length=16, choices=CHOICES
    )

    dynamic_panels = [({"field_type": "section"}, ["label", "help_text"])]


class FieldsetFormBuilder(FormBuilder):
    def __init__(self, fields):
        """
        Assign the `fields` as a subset of the fields, excluding fieldset types.
        Assign the `all_fields` as the raw fields to be used when generating the
        fieldset data.
        """
        self.all_fields = fields
        self.fields = fields.exclude(field_type="section")

    def prepare_get_fieldsets(self, allow_empty=False, field_type="section"):
        """
        Prepare a function which will have an array fieldset data that contains
        the keys for the fields in that fieldset and the `options` + `id` for the fieldset.
        This function will be called as an instance method on the Form and can be accessed
        within the template as `form.get_fieldsets` which will return an array of tuples
        where the first item is an array of fields and the second item is the fieldset data.
        """

        fieldsets = [[[], {}]]

        for field in self.all_fields:
            is_section = field.field_type == field_type

            if is_section:
                options = self.get_field_options(field)
                options["id"] = f"fieldset-{field.clean_name}"
                fieldsets.append([[], options])
            else:
                fieldsets[-1][0].append(field.clean_name)

        def get_fieldsets(form):

            return [
                (
                    [form[field] for field in fields],
                    options,
                )
                for fields, options in fieldsets
                if bool(fields) or bool(options and allow_empty)
            ]

        return get_fieldsets

    @property
    def formfields(self):
        """
        Prepare a get_fieldsets method to the generated form class so that
        it can be used within templates and access the form for the final
        field content.
        """
        formfields = super().formfields
        formfields["get_fieldsets"] = self.prepare_get_fieldsets()
        return formfields


class DynamicInlinePanel(InlinePanel):

    template = "base/edit_handlers/dynamic_inline_panel.html"

    def render(self):

        for child in self.children:

            for check, shown_fields in getattr(child.model, "dynamic_panels", []):

                is_dynamic = True
                for key, value in check.items():
                    if getattr(child.instance, key, None) != value:
                        is_dynamic = False

            if is_dynamic:

                for field_panel in child.children:
                    if field_panel.field_name not in shown_fields:

                        field_panel.form[
                            field_panel.field_name
                        ].field.widget = forms.HiddenInput()

                child.children = [
                    field_child
                    for field_child in child.children
                    if field_child.field_name in shown_fields
                ]

        formset = render_to_string(
            self.template,
            {
                "self": self,
                "can_order": self.formset.can_order,
            },
        )

        original_js = self.render_js_init()

        self.formset.prefix = f"{self.formset.prefix}-X"
        # self.empty_child.form.prefix = f"{self.empty_child.form.prefix}-X"
        other_js = self.render_js_init()

        # argh javascript!
        # buildExpandingFormset takes a single prefix
        # empty form is based on that
        # including the button id is also based on that
        # unless the empty thing is a wrapper and allows the choice of section or field
        # initially hidden
        # pass in an onAdd to the InlinePanel
        # which will get called after the empty template is converted into an object
        # I wish it were simpler!

        return widget_with_script(
            formset, " ".join([original_js, other_js, "console.log('foo');"])
        )
        # return super().render()

    def render_js_init(self):
        return mark_safe(
            render_to_string(
                self.js_template,
                {
                    "self": self,
                    "can_order": self.formset.can_order,
                },
            )
        )

    #     return [super().render_js_init(), super.render_js_init()].join(" ")


class FormPage(AbstractEmailForm):
    form_builder = FieldsetFormBuilder

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
        DynamicInlinePanel("form_fields", label="Form fields"),
        # InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text", classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    def get_form_fields(self, form=False):
        form_fields = super().get_form_fields()

        if form:
            return form_fields

        return form_fields.exclude(field_type="section")

    def get_form_class(self):
        fb = self.form_builder(self.get_form_fields(form=True))
        return fb.get_form_class()

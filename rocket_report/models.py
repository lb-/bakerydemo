from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel


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

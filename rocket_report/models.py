from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
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
        InlinePanel("rocket_reports", label="Rocket Reports"),
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

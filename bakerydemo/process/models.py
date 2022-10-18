from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from .blocks import StepsStreamBlock



class ProcessStart(models.Model):
    """
    Store the way a process starts as a Django model.
    """

    process = ParentalKey(
        "Process",
        related_name="start",
        null=True,
        on_delete=models.SET_NULL
    )

    title = models.CharField(blank=True, max_length=255)

    panels = [
        FieldPanel("title")
    ]


@register_snippet
class Process(ClusterableModel):
    """
    Stores a business process with the goal of aligning with BPMN basics.
    """

    title = models.CharField(max_length=100)
    description = models.TextField(
        help_text="Description of this process",
        blank=True,
    )
    steps = StreamField(
        StepsStreamBlock(),
        verbose_name="Steps",
        help_text="The steps this process takes towards its end",
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        InlinePanel("start", min_num=1, max_num=1),
        FieldPanel("steps"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Processes"

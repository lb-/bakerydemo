from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from .blocks import StartStreamBlock, StepsStreamBlock



@register_snippet
class Process(models.Model):
    """
    Stores a business process with the goal of aligning with BPMN basics.
    """

    title = models.CharField(max_length=100)
    description = models.TextField(
        help_text="Description of this process",
        blank=True,
    )
    start = StreamField(
        StartStreamBlock,
        verbose_name="Start",
        help_text="How does this process start?",
        blank=True,
        use_json_field=True,
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
        FieldPanel("start"),
        FieldPanel("steps"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Processes"

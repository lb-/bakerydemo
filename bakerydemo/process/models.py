from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import PreviewableMixin, RevisionMixin
from wagtail.snippets.models import register_snippet

from .blocks import StartStreamBlock, StepsStreamBlock



@register_snippet
class Process(PreviewableMixin, RevisionMixin, models.Model):
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

    def get_preview_template(self, request, mode_name):
        print('get_preview_template', request)
        return "process/previews/process.html"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Processes"

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

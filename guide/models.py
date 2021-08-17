import json
import re

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.models import Orderable


class GuideStep(models.Model):
    """
    Each step is a model to represent the step used by
    https://shepherdjs.dev/docs/Step.html
    This is an abstract model as `GuideRelatedStep` will be used for the actual model with a relation
    """

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    element = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("text"),
        FieldPanel("element"),
    ]

    class Meta:
        abstract = True


class GuideRelatedStep(Orderable, GuideStep):
    """
    Creates an orderable (user can re-order in the admin) and related 'step'
    Will be a many to one relation against `Guide`
    """

    guide = ParentalKey("guide.Guide", on_delete=models.CASCADE, related_name="steps")


class Guide(ClusterableModel):
    """
    `ClusterableModel` used to ensure that this model can have orderable relations
    using the modelcluster library (similar to ForeignKey).
    edit_handler
    """

    title = models.CharField(max_length=255)
    # steps - see GuideRelatedStep
    url_path = models.CharField(max_length=255, blank=True)

    content_panels = [
        FieldPanel("title"),
        InlinePanel("steps", label="Steps", min_num=1),
    ]

    settings_panels = [
        FieldPanel("url_path"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(settings_panels, heading="Settings"),
        ]
    )

    @classmethod
    def get_data_for_request(cls, request):
        """
        Returns a dict with data to be sent to the client (for the shepherd.js library)
        """

        path_to_match = re.sub("[\d]+", "#", request.path)

        guide = cls.objects.filter(url_path=path_to_match).first()

        if guide:
            steps = [
                {
                    "title": step.title,
                    "text": step.text,
                    "element": step.element,
                }
                for step in guide.steps.all()
            ]

            data = {"steps": steps, "title": guide.title}

            value_json = json.dumps(
                data,
                separators=(",", ":"),
            )

            data["value_json"] = value_json

            return data

        return None

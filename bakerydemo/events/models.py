from django.db import models

from modelcluster.fields import ParentalKey
from recurrence.fields import RecurrenceField

from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel, InlinePanel)
from wagtail.core.models import Page, Orderable


class ContainerFieldRowPanel(FieldRowPanel):
    # template = "wagtailadmin/edit_handlers/field_row_panel.html"
    template = "events/edit_handlers/container_field_row_panel.html"


class ConferencePage(Page):
    content_panels = Page.content_panels + [
        ContainerFieldRowPanel([InlinePanel('events', min_num=1)]),
    ]


class Event(Orderable, models.Model):
    page = ParentalKey(
        'events.ConferencePage',
        related_name='events',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    recurrences = RecurrenceField(null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('recurrences'),
    ]
    
    def __str__(self):
        return self.name
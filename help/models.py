from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


# class HelpUrlName(models.Model):
#     name = models.CharField(max_length=255)


class HelpArticle(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    body = RichTextField()
    url_name = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('url_name'),
        FieldPanel('body')
    ]

    def __str__(self):
        return self.title + " (Help article)"

    class Meta:
        verbose_name_plural = 'Help articles'

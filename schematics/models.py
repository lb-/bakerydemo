from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
)
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from .edit_handlers import (
    SchematicEditHandler,
    SchematicImageChooserPanel,
)


@register_snippet
class Schematic(index.Indexed, ClusterableModel):
    title = models.CharField("Title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        SchematicImageChooserPanel("image"),
        InlinePanel("points", heading="Points", label="Point"),
    ]

    edit_handler = SchematicEditHandler(panels)

    def __str__(self):
        title = getattr(self, "title", "Schematic")
        return f"Schematic - {title} ({self.pk})"

    class Meta:
        verbose_name_plural = "Schematics"
        verbose_name = "Schematic"


class SchematicPoint(Orderable, models.Model):
    schematic = ParentalKey(
        "schematics.Schematic",
        on_delete=models.CASCADE,
        related_name="points",
    )

    label = models.CharField("Label", max_length=254)

    x = models.DecimalField(
        verbose_name="X →",
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
    )

    y = models.DecimalField(
        verbose_name="Y ↑",
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0)],
    )

    panels = [
        FieldPanel("label"),
        FieldRowPanel(
            [
                FieldPanel(
                    "x", widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0})
                ),
                FieldPanel(
                    "y", widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0})
                ),
            ]
        ),
    ]

    def __str__(self):
        schematic_title = getattr(self.schematic, "title", "Schematic")
        return f"{schematic_title} - {self.label}"

    class Meta:
        verbose_name_plural = "Points"
        verbose_name = "Point"


class ProductPage(Page):

    schematic = models.ForeignKey(
        "schematics.Schematic",
        null=True,
        on_delete=models.SET_NULL,
        related_name="product_page_schematic",
    )

    content_panels = Page.content_panels + [SnippetChooserPanel("schematic")]

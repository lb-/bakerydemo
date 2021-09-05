from django.utils.functional import cached_property

from wagtail.images.blocks import ChooserBlock, ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock


class RestrictedDocumentChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from wagtail.documents.models import Document

        return Document

    @cached_property
    def widget(self):
        from .widgets import RestrictedDocumentChooser

        return RestrictedDocumentChooser()

    def get_form_state(self, value):
        return self.widget.get_value_data(value)


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """

    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    doc_block = RestrictedDocumentChooserBlock(accept="svg,md")  # uses accept kwarg
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph", template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks",
        icon="fa-s15",
        template="blocks/embed_block.html",
    )

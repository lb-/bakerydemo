from wagtail.images.blocks import ImageChooserBlock
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


class SpecificDocumentChooserBlock(DocumentChooserBlock):
    """
    Existing DocumentChooserBlock with the ability to add widget attrs based on the
    accept kwarg, anything on self.widget.attrs will be added to the hidden
    input field (so be careful what key is used).
    """

    def __init__(self, accept=None, **kwargs):
        super().__init__(**kwargs)

        self.widget.attrs["accept"] = accept


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    doc_block = SpecificDocumentChooserBlock(accept="svg,md")  # uses accept kwarg
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

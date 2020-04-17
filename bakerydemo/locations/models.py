from itertools import chain

from django import forms

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.admin.widgets import AdminTagWidget

from wagtail.core.blocks import CharBlock, FieldBlock, StructBlock, RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

class TagsBlock(FieldBlock):
    """
    Basic Stream Block that will use the Wagtail tags system.
    Stores the tags as simple strings only.
    """

    def __init__(self, required=False, help_text=None, **kwargs):
        self.field = forms.CharField(widget=AdminTagWidget)
        super().__init__(**kwargs)


class MapBlock(StructBlock):
    title = CharBlock(label="Title", required=False)
    content = RichTextBlock(label="Content", required=False)
    tags = TagsBlock(label="Tags", required=False)

    class Meta:
        icon = 'site'


class LocationPage(Page):
    """
    Detail for a specific location.
    """

    # ... other fields

    # this is the stream field added
    map_info = StreamField([('Map', MapBlock(required=False))], blank=True)

    @property
    def get_tags(self):
        """
        Helpful property to pull out the tags saved inside the struct value
        Important: makes some hard assumptions about the names & structure
        Does not get the id of the tag, only the strings as a list
        """

        tags_all = [block.value.get('tags', '').split(',') for block in self.test_b]

        tags = list(chain.from_iterable(tags_all))

        return tags

    # Fields to show to the editor in the admin view
    content_panels = [
        FieldPanel('title', classname="full"),
        StreamFieldPanel('map_info'),
        # ... others
    ]

    # ... rest of page model

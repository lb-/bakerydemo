from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

class HalloTestPage(Page):
    body = RichTextField(editor='legacy', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

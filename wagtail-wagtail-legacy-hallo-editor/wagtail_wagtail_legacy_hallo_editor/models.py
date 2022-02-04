from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

class HalloPage(Page):
    body = RichTextField(editor='legacy', blank=True)
    # body_hallo = RichTextField(editor='hallo', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        # FieldPanel('body_hallo', classname='full'),
    ]

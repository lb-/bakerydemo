from django.forms import Media, widgets

from django.conf.urls.static import static


class WryneckRichTextArea(widgets.TextInput):
    # template_name = "widgets/wryneck_rich_text_area.html"
    is_hidden = False

    # this class's constructor accepts a 'features' kwarg
    accepts_features = True

    # commenting
    show_add_comment_button = True

    def __init__(self, *args, **kwargs):
        print('init??')
        self.features = kwargs.pop("features", None)
        kwargs.pop("options", None)

        self.options = {}
        self.plugins = []

        default_attrs = {"data-controller": "wryneck"}
        attrs = kwargs.get("attrs")
        if attrs:
            default_attrs.update(attrs)
        kwargs["attrs"] = default_attrs

        super().__init__(*args, **kwargs)

    @property
    def media(self):
        # not handling plugins yet - see Wagtail draftail implementation later
        return Media(
            css={'all': ('wryneck/main.css',)},
            js=('wryneck/wryneck.iife.js',)
        )

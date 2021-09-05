from wagtail.admin.edit_handlers import MultiFieldPanel


class ZenModeMultiFieldPanel(MultiFieldPanel):

    template = "base/edit_handlers/zen_mode_multi_field_panel.html"

    def classes(self):
        classes = super().classes()
        classes.append("zen-mode-panel")
        return classes

from django.utils.html import format_html

from wagtail.admin.edit_handlers import MultiFieldPanel, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.widgets import AdminImageChooser


class AdminPreviewImageChooser(AdminImageChooser):
    """
    Generates a larger version of the AdminImageChooser
    Currently limited to showing the large image on load only.
    """

    def get_value_data(self, value):
        value_data = super().get_value_data(value)

        if value_data:
            image = self.image_model.objects.get(pk=value_data["id"])
            # note: the image string here should match what is used in the template
            preview_image = image.get_rendition("width-1920")
            value_data["preview"] = {
                "width": preview_image.width,
                "height": preview_image.height,
                "url": preview_image.url,
            }

        return value_data


class SchematicImageChooserPanel(ImageChooserPanel):
    def widget_overrides(self):
        return {
            self.field_name: AdminPreviewImageChooser(
                attrs={
                    "data-schematic-edit-handler-target": "imageInput",
                }
            )
        }


class SchematicEditHandler(ObjectList):
    template = "schematics/edit_handlers/schematic_edit_handler.html"

    def get_form_class(self):
        form_class = super().get_form_class()
        return type(
            form_class.__name__,
            (form_class,),
            {"Media": self.Media},
        )

    class Media:
        css = {"all": ("css/schematic-edit-handler.css",)}
        js = ("js/schematic-edit-handler.js",)


class SchematicPointPanel(MultiFieldPanel):
    template = "schematics/edit_handlers/schematic_point_panel.html"

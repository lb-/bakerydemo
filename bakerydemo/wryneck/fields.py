# import json

# from django.core.exceptions import ImproperlyConfigured
# from django.core.serializers.json import DjangoJSONEncoder
# from django.core.validators import MaxLengthValidator
# from django.db import models
# from django.db.models.fields.json import KeyTransform
# from django.utils.encoding import force_str

# from wagtail.blocks import Block, BlockField, StreamBlock, StreamValue
# from wagtail.rich_text import (
#     RichTextMaxLengthValidator,
#     extract_references_from_rich_text,
#     get_text_for_indexing,
# )


# class RichTextField(models.TextField):
#     def __init__(self, *args, **kwargs):
#         # 'editor' and 'features' are popped before super().__init__ has chance to capture them
#         # for use in deconstruct(). This is intentional - they would not be useful in migrations
#         # and retrospectively adding them would generate unwanted migration noise
#         self.editor = kwargs.pop("editor", "default")
#         self.features = kwargs.pop("features", None)

#         super().__init__(*args, **kwargs)

#     def clone(self):
#         name, path, args, kwargs = self.deconstruct()
#         # add back the 'features' and 'editor' kwargs that were not preserved by deconstruct()
#         kwargs["features"] = self.features
#         kwargs["editor"] = self.editor
#         return self.__class__(*args, **kwargs)

#     def formfield(self, **kwargs):
#         from wagtail.admin.rich_text import get_rich_text_editor_widget

#         defaults = {
#             "widget": get_rich_text_editor_widget(self.editor, features=self.features)
#         }
#         defaults.update(kwargs)
#         field = super().formfield(**defaults)

#         # replace any MaxLengthValidators with RichTextMaxLengthValidators to ignore tags
#         for (i, validator) in enumerate(field.validators):
#             if isinstance(validator, MaxLengthValidator):
#                 field.validators[i] = RichTextMaxLengthValidator(
#                     validator.limit_value, message=validator.message
#                 )

#         return field

#     def get_searchable_content(self, value):
#         # Strip HTML tags to prevent search backend from indexing them
#         source = force_str(value)
#         return [get_text_for_indexing(source)]

#     def extract_references(self, value):
#         yield from extract_references_from_rich_text(force_str(value))

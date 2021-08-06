from django.db.models import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from wagtail.images import get_image_model

image_model = get_image_model()


@receiver(pre_delete, sender=image_model, dispatch_uid='post_pre_delete_signal')
def protect_posts(sender, instance, using, **kwargs):
    raise ProtectedError('Only unpublished posts can be deleted.', instance)

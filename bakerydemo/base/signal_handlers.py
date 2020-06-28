from django.db.models.signals import pre_save

from wagtail.images import get_image_model
from wagtail.images.rect import Rect


def pre_save_image_add_auto_focal_point(instance, **kwargs):
    # Make sure the image doesn't already have a focal point
    # add any other logic here based on the image about to be saved

    if not instance.has_focal_point():
        # this will run on update and creation, check instance.pk to see if this is new

        # generate a focal_point - via Rect(left, top, right, bottom)
        focal_point = Rect(15, 15, 150, 150)

        # Set the focal point
        instance.set_focal_point(focal_point)


def register_signal_handlers():
    # important: this function must be called at the app ready

    Image = get_image_model()

    pre_save.connect(pre_save_image_add_auto_focal_point, sender=Image)

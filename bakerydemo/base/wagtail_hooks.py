from django.urls import resolve
from urllib.parse import urlparse
from wagtail.core import hooks
from wagtail.core.models import Page


@hooks.register('construct_image_chooser_queryset')
def show_images_for_specific_collections_on_page_editing(images, request):

    # first - pull out the referrer for this current AJAX call
    http_referrer = request.META.get('HTTP_REFERER', None) or '/'

    # second - use django utils to find the matched view
    match = resolve(urlparse(http_referrer)[2])

    # if we are editing a page we can restrict the available images
    if (match.app_name is 'wagtailadmin_pages') and (match.url_name is 'edit'):
        page = Page.objects.get(pk=match.args[0])

        # important: wrap in a try/except as this may not be implemented on all pages
        image_collection_id = page.specific_class.get_image_collection()

        # return filtered images
        return images.filter(collection=image_collection_id)

    return images

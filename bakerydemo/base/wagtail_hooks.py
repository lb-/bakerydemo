from django.conf.urls import url
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from wagtail.admin.widgets import PageListingButton
from wagtail.core import hooks


@csrf_exempt # not recommended - but helpful to get to the POC stage
@require_http_methods(["POST"])
def regnerate_admin_features(request):
    page_pk = request.GET.get('id', '')
    # do whatever you need here with the PK to process the action

    return HttpResponse(
        "Success/Error handling goes here",
        content_type="text/plain")

@hooks.register('register_admin_urls')
def urlconf_time():
  return [
    url(r'^regenerate_geo_features/$', regnerate_admin_features, name='regenerate_geo_features'),
  ]

@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):

    attrs = {
        'data-id': page.pk, # note - may want to html encode this for a more secure implementation
    }

    yield PageListingButton(
        'Regenerate Geo Features',
        reverse('regenerate_geo_features'),
        attrs=attrs,
        classes=["action-regenerate-geo-features"],
        priority=100
    )

@hooks.register('insert_global_admin_js')
def global_admin_js():
    # note - this is very rough, no error, loading or sucess messaging
    # reminder - using format_html means all `{` must be written as `{{`
    return format_html(
        """
        <script>
        const onClickHandler = function(event) {{
            event.preventDefault(); // ensure the hash does not change
            const url = event.target.href + '?id=' + event.target.dataset.id;
            console.log('button clicked - about to POST to URL:', url);
            fetch(url, {{
                method: 'POST', // or 'PUT'
            }})
        }};

        window.addEventListener('DOMContentLoaded', function(event) {{
            const actionButtons = Array.from(document.getElementsByClassName('action-regenerate-geo-features'));

            actionButtons.forEach(function(element) {{
                element.addEventListener('click', onClickHandler);
            }});
        }});
        </script>
        """,
    )

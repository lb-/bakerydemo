from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from hallo import (
    HalloFormatPlugin, HalloHeadingPlugin, HalloListPlugin, HalloPlugin)
from wagtail.admin.rich_text.converters.editor_html import (
    LinkTypeRule, PageLinkHandler, WhitelistRule)
from wagtail.core import hooks
from wagtail.core.whitelist import allow_without_attributes, attribute_rule, check_url


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [
        path('jsi18n/', JavaScriptCatalog.as_view(packages=['wagtail_wagtail_legacy_hallo_editor']), name='javascript_catalog'),

        # Add your other URLs here, and they will appear under `/admin/wagtail_legacy_hallo_editor/`
        # Note: you do not need to check for authentication in views added here, Wagtail does this for you!
    ]

    return [
        path(
            "wagtail_legacy_hallo_editor/",
            include(
                (urls, "wagtail_wagtail_legacy_hallo_editor"),
                namespace="wagtail_wagtail_legacy_hallo_editor",
            ),
        )
    ]


@hooks.register('register_rich_text_features')
def register_core_features(features):
    # Hallo.js
    features.register_editor_plugin(
        'hallo', 'hr',
        HalloPlugin(
            name='hallohr',
            js=['wagtailadmin/js/hallo-plugins/hallo-hr.js'],
            order=45,
        )
    )
    features.register_converter_rule('editorhtml', 'hr', [
        WhitelistRule('hr', allow_without_attributes)
    ])

    features.register_editor_plugin(
        'hallo', 'link',
        HalloPlugin(
            name='hallowagtaillink',
            js=[
                'wagtailadmin/js/page-chooser-modal.js',
                'wagtailadmin/js/hallo-plugins/hallo-wagtaillink.js',
            ],
        )
    )

    features.register_converter_rule('editorhtml', 'link', [
        WhitelistRule('a', attribute_rule({'href': check_url})),
        LinkTypeRule('page', PageLinkHandler),
    ])

    features.register_editor_plugin(
        'hallo', 'bold', HalloFormatPlugin(format_name='bold')
    )

    features.register_converter_rule('editorhtml', 'bold', [
        WhitelistRule('b', allow_without_attributes),
        WhitelistRule('strong', allow_without_attributes),
    ])

    features.register_editor_plugin(
        'hallo', 'italic', HalloFormatPlugin(format_name='italic')
    )

    features.register_converter_rule('editorhtml', 'italic', [
        WhitelistRule('i', allow_without_attributes),
        WhitelistRule('em', allow_without_attributes),
    ])

    headings_elements = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    headings_order_start = HalloHeadingPlugin.default_order + 1
    for order, element in enumerate(headings_elements, start=headings_order_start):
        features.register_editor_plugin(
            'hallo', element, HalloHeadingPlugin(element=element, order=order)
        )
        features.register_converter_rule('editorhtml', element, [
            WhitelistRule(element, allow_without_attributes)
        ])

    features.register_editor_plugin(
        'hallo', 'ol', HalloListPlugin(list_type='ordered')
    )
    features.register_converter_rule('editorhtml', 'ol', [
        WhitelistRule('ol', allow_without_attributes),
        WhitelistRule('li', allow_without_attributes),
    ])

    features.register_editor_plugin(
        'hallo', 'ul', HalloListPlugin(list_type='unordered')
    )
    features.register_converter_rule('editorhtml', 'ul', [
        WhitelistRule('ul', allow_without_attributes),
        WhitelistRule('li', allow_without_attributes),
    ])

    # define a hallo.js plugin to use when the 'embed' feature is active
    features.register_editor_plugin(
        'hallo', 'embed',
        HalloPlugin(
            name='hallowagtailembeds',
            js=[
                'wagtailembeds/js/embed-chooser-modal.js',
                'wagtailembeds/js/hallo-plugins/hallo-wagtailembeds.js',
            ],
        )
    )

    # define a hallo.js plugin to use when the 'image' feature is active
    features.register_editor_plugin(
        'hallo', 'image',
        HalloPlugin(
            name='hallowagtailimage',
            js=[
                'wagtailimages/js/image-chooser-modal.js',
                'wagtailimages/js/hallo-plugins/hallo-wagtailimage.js',
            ],
        )
    )

    features.register_editor_plugin(
        'hallo', 'document-link',
        HalloPlugin(
            name='hallowagtaildoclink',
            js=[
                'wagtaildocs/js/document-chooser-modal.js',
                'wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js',
            ],
        )
    )
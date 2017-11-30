import os

import docutils

from django.http import HttpResponse
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import render

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from wagtail.wagtailcore import hooks

from bakerydemo.breads.models import Country, BreadIngredient, BreadType
from bakerydemo.base.models import People, FooterText

'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.wagtailstyleguide',
   ...
)

or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''


class BreadIngredientAdmin(ModelAdmin):
    # These stub classes allow us to put various models into the custom "Wagtail Bakery" menu item
    # rather than under the default Snippets section.
    model = BreadIngredient


class BreadTypeAdmin(ModelAdmin):
    model = BreadType


class BreadCountryAdmin(ModelAdmin):
    model = Country


class BreadModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bread Categories'
    menu_icon = 'fa-suitcase'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (BreadIngredientAdmin, BreadTypeAdmin, BreadCountryAdmin)


class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-users'  # change as required
    list_display = ('first_name', 'last_name', 'job_title', 'thumb_image')


class FooterTextAdmin(ModelAdmin):
    model = FooterText


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bakery Misc'
    menu_icon = 'fa-cutlery'  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PeopleModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(BreadModelAdminGroup)
modeladmin_register(BakeryModelAdminGroup)

# mucking around with idea of putting user editors manual inside wagtail


def admin_editors_manual_view(request):
    # dir = os.listdir('../')
    # dir =
    location_of_file = os.path.dirname(hooks.__file__)
    location_of_docs = os.path.join(
        location_of_file, '..', '..', './docs', './editor_manual'
    )
    dir = os.listdir(
        location_of_docs
        # ['administrator_tasks', 'browser_issues.rst', 'documents_images_snippets',
        # 'editing_existing_pages.rst', 'finding_your_way_around', 'getting_started.rst',
        # 'index.rst', 'intro.rst', 'managing_redirects.rst', 'new_pages']
    )
    file_path = os.path.join(location_of_docs, './index.rst')
    file = open(file_path, 'r')
    contents = docutils.core.publish_parts(file.read(), writer_name='html')
    print('dir', dir)
    return render(request, 'wagtailmanual/base.html', {
        'title': 'Editors Manual',
        'something': dir,
        'contents': contents,
    })


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(
            r'^editors_manual/$',
            admin_editors_manual_view,
            name='editors-manual'
        ),
    ]


@hooks.register('register_admin_menu_item')
def register_editors_manual_item():
    return MenuItem(
        'Manual',
        reverse('editors-manual'),
        classnames='icon icon-folder-inverse',
        order=10000
    )

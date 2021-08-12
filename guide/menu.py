import re

from django.utils.safestring import mark_safe

from wagtail.contrib.modeladmin.menus import ModelAdminMenuItem

from .models import Guide

class GuideAdminMenuItem(ModelAdminMenuItem):

    def get_context(self, request):
        context = super().get_context(request)
        path_to_match = re.sub('[\d]+', '#', request.path)
        print('path_to_match', path_to_match)
        guide = Guide.objects.filter(url_path=path_to_match).first()

        if guide:
            context['attr_string'] = context['attr_string'] + ' ' + mark_safe('id=start-tour')
            context['classnames'] = context['classnames'] + ' help-available'

            steps = [
                {
                    'title': step.title,
                    'text': step.text,
                    'element': step.element
                } for step in guide.steps.all()
            ]

            context['guide_options'] = {'steps': steps}

        return context

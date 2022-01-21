from wagtail.core import hooks

from .views import StimulusPanel

@hooks.register('construct_homepage_panels')
def add_stimulus_panel(request, panels):
    panels.append(StimulusPanel())


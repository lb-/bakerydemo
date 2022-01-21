from wagtail.admin.ui.components import Component

class StimulusPanel(Component):
    order = 10
    template_name = 'ui/panels/stimulus.html'


my_welcome_panel = StimulusPanel()

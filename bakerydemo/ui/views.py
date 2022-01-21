from wagtail.admin.ui.components import Component

class StimulusPanel(Component):
    order = 10
    template_name = 'ui/panels/stimulus.html'

    # class Media:
    #     js = ('https://unpkg.com/@hotwired/stimulus/dist/stimulus.js',)


my_welcome_panel = StimulusPanel()

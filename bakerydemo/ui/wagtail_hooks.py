from django.utils.safestring import mark_safe

from wagtail.core import hooks

from .views import StimulusPanel


@hooks.register('construct_homepage_panels')
def add_stimulus_panel(request, panels):
    panels.append(StimulusPanel())

@hooks.register('insert_global_admin_js')
def add_stimulus_module():
    return mark_safe(
    """
    <script type="module">
      import { Application, Controller } from "https://unpkg.com/@hotwired/stimulus/dist/stimulus.js";
      window.Stimulus = Application.start();
      window.Controller = Controller;

      // future - base Wagtail controllers would be registered first

      // future - Stimulus.debug = true/false (based on env)

      // dispatch event to hook custom controller registrations in
      var event = new CustomEvent('wagtail:stimulus-init', { bubbles: true });
      console.log('Stimulus application loaded - firing wagtail:stimulus-init', event);
      document.body.dispatchEvent(event);
    </script>
    """
    )
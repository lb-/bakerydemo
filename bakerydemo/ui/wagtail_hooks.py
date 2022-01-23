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
      window.wagtail.stimulus = {};
      window.wagtail.stimulus.Application = Application.start();
      window.wagtail.stimulus.Controller = Controller;
      // note: this may not be the best API to use, just explored the available attributes.
      // the intent is that this is similar to getControllerByNameAndIdentifier but without the name part
      window.wagtail.stimulus.getControllerByIdentifier = (identifier) => window.wagtail.stimulus.Application.router.modulesByIdentifier.get(identifier).definition.controllerConstructor;

      // future - base Wagtail controllers would be registered first

      /** Basic Hello controller to demo a Wagtail introduced controller
       * that can be pulled in, extended and override existing behaviour object oriented style.
       */
      class Hello extends Controller {
        static targets = [ "name" ];
        static values = { label: { default: '', type: String }, replace: { default: false, type: Boolean } };

        doLog() {
          console.log('hello stimulus', this.element);
        }

        connect() {
          this.doLog(name);
        }
      }

      window.wagtail.stimulus.Application.register('hello', Hello);

      // future - Stimulus.debug = true/false (based on env)

      // dispatch event to hook custom controller registrations in
      var event = new CustomEvent('wagtail:stimulus-init', { bubbles: true });
      console.log('Stimulus application loaded - firing wagtail:stimulus-init', event);
      document.body.dispatchEvent(event);
    </script>
    """
    )
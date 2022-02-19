from django.conf import settings
from django.utils.html import format_html

from wagtail.core import hooks


@hooks.register("insert_editor_js")
def insert_stimulus_js():
    return format_html(
        """
        <script type="module">
            import {{ Application, Controller }} from "https://unpkg.com/@hotwired/stimulus/dist/stimulus.js";
            const Stimulus = Application.start();
            {}
            window.dispatchEvent(new CustomEvent('stimulus:init', {{ detail: {{ Stimulus, Controller }} }}));
        </script>
        """,
        # set Stimulus to debug mode if running Django in DEBUG mode
        "Stimulus.debug = true;" if settings.DEBUG else "",
    )

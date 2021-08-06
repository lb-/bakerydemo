from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'bakerydemo.base'  # must match the configured app name

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import bakerydemo.base.signals

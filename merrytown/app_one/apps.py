from django.apps import AppConfig


class AppOneConfig(AppConfig):
    name = 'app_one'
    def ready(self):
        import app_one.signals

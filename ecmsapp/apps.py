from django.apps import AppConfig


class EcmsappConfig(AppConfig):
    name = 'ecmsapp'

    def ready(self):
        import ecmsapp.signals

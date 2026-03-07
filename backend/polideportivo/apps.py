from django.apps import AppConfig

class PolideportivoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polideportivo'

    def ready(self):
        import polideportivo.signals
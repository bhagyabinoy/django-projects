from django.apps import AppConfig


class UserandeventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userandevent'

    def ready(self):
        import userandevent.signals 
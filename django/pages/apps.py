from django.apps import AppConfig
from django.db.models.signals import post_save


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        import pages.signals
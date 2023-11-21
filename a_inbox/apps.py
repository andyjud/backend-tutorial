from django.apps import AppConfig


class AInboxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_inbox'
    
    def ready(self):
        import a_inbox.signals

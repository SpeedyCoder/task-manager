from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        # Register rules
        import tasks.rules
        import tasks.templatetags.helpers

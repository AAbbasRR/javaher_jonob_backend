from django.apps import AppConfig


class AppFactorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_factor"

    def ready(self):
        import app_factor.signals.factor
        import app_factor.signals.factor_items

from django.apps import AppConfig


class InvestmentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investment_app'

    def ready(self) -> None:
        from investment_app import signals
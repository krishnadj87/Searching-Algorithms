from django.apps import AppConfig


class EmployeesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees_app'
    
    def ready(self):
        import employees_app.signals
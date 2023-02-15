from django.contrib import admin
from .models import Employee,Department,Profile



# Department model registing here
@admin.register(Department)
class DepartmentModel(admin.ModelAdmin):
    list_display  = ('id', 'name')

@admin.register(Employee)
class EmployeeModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'dept', 'salary', 'image')


# from .models import Employee
@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_display = ('user', 'bio', 'pic', 'address')


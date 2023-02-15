from django.urls import path
from .views import *  # import all views of employee-app
from .api_views import EmployeeAPI

urlpatterns = [
    path('', homepage, name='homepage'),
    path('not/found-errors/', not_found_page, name='page_not_found'),
    path('custom-search/<str:by>/',search_employees, name='employeesFilter'),
    path('select/<str:nm>/', dynamic, name='details'),

    path('add-employee/',AddEmployeeView.as_view(), name='addEmployees'),
    path("update-employee/<int:id>/", UpdateeEmployee.as_view(), name="update_employee"),
    path('delete-employee/<int:id>/',DeleteEmployee.as_view(), name='deleteEmployee'),

    # employee api view here
    path('employees-api/',EmployeeAPI.as_view(), name='employees_api' ),
    


]

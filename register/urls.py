from . import views
from django.urls import path

app_name = 'register'

urlpatterns = [
    path('', views.index, name='employee_list'),
    path('employees/', views.EmployeesListView.as_view(), name='employee_list'),
    path('employee-detail/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/upload-records/', views.upload_records, name='upload_records'),
]

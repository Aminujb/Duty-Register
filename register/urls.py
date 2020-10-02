from . import views
from django.urls import path

app_name = 'register'

urlpatterns = [
    # path('', views.index, name='employee_list'),
    path('search/', views.SearchEmployeesView.as_view(), name='search_results'),
    path('', views.EmployeesListView.as_view(), name='employee_list'),
    path('employee-detail/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/upload-records/', views.upload_records, name='upload_records'),
    path('employees/create-pass/', views.PassCreateView.as_view(), name='create_pass'),
    path('employees/pass-history/', views.PassListView.as_view(), name='pass_history'),
    path('employees/upload-pass-records/', views.upload_pass_records, name='upload_pass_records'),
]

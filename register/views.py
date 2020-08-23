from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView
from register.models import Employee
from django.shortcuts import render


# Create your views here.
def index(request):
    return TemplateResponse(request, 'register/index.html')


class EmployeesListView(ListView):
    model = Employee
    template_name = 'register/employee_list.html'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'register/employee_detail.html'

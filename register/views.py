from django.db.models import Q
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
from register.models import Employee
from django.shortcuts import render, redirect
from register.forms import UploadRecords


# Create your views here.
def index(request):
    return TemplateResponse(request, 'register/index.html')


class EmployeesListView(ListView):
    model = Employee
    template_name = 'register/employee_list.html'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'register/employee_detail.html'


class SearchEmployeesView(ListView):
    model = Employee
    template_name = 'register/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(SearchEmployeesView, self).get_context_data(**kwargs)
        context["search_word"] = self.request.GET.get('q')
        context["search_not_found"] = 'No such employee record available'
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Employee.objects.filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query) | Q(middle_name__icontains=query)
        )
        return object_list


def upload_records(request, next_item='register:employee_list'):
    if request.method == 'POST':
        form = UploadRecords(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse(next_item,))
        else:
            form = UploadRecords()
            render(request, 'register/upload_records.html',
                   {"form": form, "next": reverse(next_item), })
    else:
        form = UploadRecords()
    return render(request, 'register/upload_records.html', {"form": form, "next": reverse(next_item),})


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from register.models import Employee, Pass
from django.shortcuts import render, redirect
from register.forms import UploadRecords, PassForm, UploadPassRecords
from django.contrib.auth.decorators import login_required


class EmployeesListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'register/employee_list.html'


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'register/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        emp = Employee.objects.get(pk=pk)
        context["pass_history"] = reversed(list(Pass.objects.filter(employee=emp)))
        return context


class SearchEmployeesView(LoginRequiredMixin, ListView):
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


@login_required()
def upload_records(request, next_item='register:employee_list'):
    if request.method == 'POST':
        form = UploadRecords(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee records uploaded successfully!')
            return redirect(reverse(next_item, ))
        else:
            form = UploadRecords()
            messages.error(request, 'Employee record upload was unsuccessful, please validate data and try again.')
            render(request, 'register/upload_records.html',
                   {"form": form, "next": reverse(next_item), })
    else:
        form = UploadRecords()
    return render(request, 'register/upload_records.html', {"form": form, "next": reverse(next_item), })


class PassCreateView(LoginRequiredMixin, CreateView):
    model = Pass
    form_class = PassForm
    template_name = "register/create_pass.html"
    success_url = reverse_lazy("register:employee_list")


class PassListView(LoginRequiredMixin, ListView):
    model = Pass
    template_name = "register/pass_list'html"


@login_required()
def upload_pass_records(request, next_item='register:pass_history'):
    if request.method == 'POST':
        form = UploadPassRecords(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pass uploaded successfully!')
            return redirect(reverse(next_item, ))
        else:
            form = UploadRecords()
            messages.error(request, 'Pass upload was unsuccessful, please validate data and try again.')
            render(request, 'register/upload_pass_records.html',
                   {"form": form, "next": reverse(next_item), })
    else:
        form = UploadPassRecords()
    return render(request, 'register/upload_pass_records.html', {"form": form, "next": reverse(next_item), })


def handler404(request, exception):
    context = {}
    response = render(request, "register/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "register/500.html", context=context)
    response.status_code = 500
    return response

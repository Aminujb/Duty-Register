"""duty_register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as login_views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('register.urls')),
    path('', include('pwa.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', never_cache(login_views.LoginView.as_view()), name='login'),
    # path('accounts/logout/', never_cache(login_views.LogoutView.as_view()), name='logout'),
    # path(
    #     'accounts/password-change/',
    #     never_cache(login_views.PasswordChangeView.as_view(
    #         success_url=reverse_lazy('register:employee_list'),
    #     )),
    #     name='password_change'
    # ),
    # path(
    #     'accounts/password-reset/',
    #     login_views.PasswordResetView.as_view(
    #         email_template_name='registration/password_reset_email.txt',
    #         html_email_template_name='registration/password_reset_email.html'
    #     ),
    #     name='password_reset'
    # ),
    # path('accounts/password-reset/done/', login_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path(
    #     'accounts/reset/<uidb64>/<token>/',
    #     login_views.PasswordResetConfirmView.as_view(
    #         template_name='selfservice/manage.html',
    #         success_url=reverse_lazy('selfservice:my_profile'),
    #         form_class=PasswordChangeForm
    #     ),
    #     name='password_reset_confirm'),
    # path('accounts/reset/done/', login_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

handler404 = 'register.views.handler404'
handler500 = 'register.views.handler500'

from django.shortcuts import redirect
from django.urls import reverse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.lock_program = True

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # next_item = 'register:employee_list'
        #
        # if self.lock_program:
        #     return redirect(next_item)
        # else:
        #     return self.get_response(request)


        # redirect(reverse(next_item))
        # Code to be executed for each request/response after
        # the view is called.
        response = self.get_response(request)
        return response
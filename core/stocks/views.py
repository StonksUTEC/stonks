from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic,View


# Create your views here.
"""
def index(request):
    return HttpResponse("Demo: Stonks - Stocks App")
"""

class IndexView(View):
    template_name = "stocks/index.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

class LoginView(View):
    template_name = "stocks/login.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class RegisterView(View):
    template_name = "stocks/register.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class AccountView(View):
    template_name = "stocks/account.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)






#Demo
class DemoView(View):
    template_name = "stocks/user_test.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

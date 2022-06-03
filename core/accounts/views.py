from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class IndexView(View):
    template_name = "stocks/index.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

class LoginView(View):
    template_name = "stocks/login.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class RegisterView(View):
    template_name = "stocks/register.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class AccountView(View):
    template_name = "stocks/account.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

class UpdateView(View):
    template_name = "stocks/update.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)




from django.urls import path, include
from . import api
from knox import views as knox_views

urlpatterns = [
    path('user/', api.UserDetailsAPI.as_view(), name="api-user"),
    path('register/', api.RegisterAPI.as_view(), name="api-register" ),
    path('login/', api.LoginAPI.as_view(), name="api-login"),
    path('logout/', knox_views.LogoutView.as_view(), name="api-logout"),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='api-logoutall'),
    path('change-password/', api.ChangePasswordAPI.as_view(), name='api-password'),
    path('change-data/', api.ChangeUserDataAPI.as_view(), name='api-change-data'),
]

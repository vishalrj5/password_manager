from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers


urlpatterns = [
    path('create_password', views.CreatePasswordAPIView.as_view()),
    path('update_password', views.UpdatePasswordAPIView.as_view()),
    path('list_password', views.GetUserPasswordsApiView.as_view()),

]

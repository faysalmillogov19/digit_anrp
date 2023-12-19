from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("", views.list, name='user_list'),
    path("signin", views.signin, name='user_signin'),
    path("signup", views.signup, name='user_signup'),
    path("signout", views.signout, name='user_signout'),

    path("user_state", views.user_state, name='user_state'),
    path("set_profil", views.set_profil, name='set_profil'),
    path("get_role/<int:user_id>", views.get_role, name='get_role'),
]
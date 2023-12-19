from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("signin/", views.signin, name='demandeur_signin'),
    path("signup/", views.signup, name='demandeur_signup'),
    path("logout/", views.signout, name='demandeur_logout'),
]

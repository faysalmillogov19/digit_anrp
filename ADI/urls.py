from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("add/", views.add, name='add_adi'),

]

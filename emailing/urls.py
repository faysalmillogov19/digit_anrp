from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	path('', views.Serverconfiguration, name="config_email"),
    #path('email_configuration', views.setServerconfiguration, name="set_email_server_configuration"),
    path('testemail', views.test, name="email_config_test"),
]

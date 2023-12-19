from django.urls import path,include, re_path
from . import views

urlpatterns = [
    path('add_adi/', views.add_adi, name='add_adi'),
    path('add_dpi/', views.add_dpi, name='add_dpi'),
    path('add_ari/', views.add_ari, name='add_ari'),
    path('add_ase/', views.add_ase, name='add_ase'),
]
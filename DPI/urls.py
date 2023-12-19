from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("add_produit/<int:id_demande>", views.add_produit, name='dpi_new_produit'),
    path("delete_produit/<int:id>", views.delete_produit, name='dpi_delete_produit'),
    path("set_produit/<int:id>", views.set_produit, name='dpi_set_produit'),

    path("list_produit/<int:id_demande>", views.list_produit, name='dpi_list_produit'),

    path("expediteur/<int:id_demande>", views.expediteur, name='dpi_expediteur'),
    path("pieces_jointes/<int:id_demande>", views.pieces_jointes, name='dpi_pieces_jointes'),
    path("recap/<int:id_demande>", views.recap, name='dpi_recap_dpi'),
    path("valid_demande/<int:id_demande>", views.valid_demande, name='dpi_valid_demande'),

]

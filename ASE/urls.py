from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("add_produit/<int:id_demande>", views.add_produit, name='ase_new_produit'),
    path("delete_produit/<int:id>", views.delete_produit, name='ase_delete_produit'),
    path("set_produit/<int:id>", views.set_produit, name='ase_set_produit'),

    path("list_produit/<int:id_demande>", views.list_produit, name='ase_list_produit'),

    path("expediteur/<int:id_demande>", views.expediteur, name='ase_expediteur'),
    path("pieces_jointes/<int:id_demande>", views.pieces_jointes, name='ase_pieces_jointes'),
    path("recap/<int:id_demande>", views.recap, name='ase_recap_ase'),
    path("valid_demande/<int:id_demande>", views.valid_demande, name='ase_valid_demande'),

    #path("get_produit/<int:id>", views.get_produit, name='get_produit'),
]

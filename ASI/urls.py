from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("add_produit/<int:id_asi>", views.add_produit, name='asi_new_produit'),
    path("delete_produit/<int:id>", views.delete_produit, name='delete_produit'),
    path("set_produit/<int:id>", views.set_produit, name='set_produit'),

    path("list_produit/<int:id_asi>", views.list_produit, name='asi_list_produit'),

    path("expediteur/<int:id_asi>", views.expediteur, name='asi_expediteur'),
    path("pieces_jointes/<int:id_asi>", views.pieces_jointes, name='asi_pieces_jointes'),
    path("recap_asi/<int:id_asi>", views.recap_asi, name='asi_recap_asi'),
    path("valid_asi/<int:id_asi>", views.valid_asi, name='asi_valid_asi'),

    path("get_produit/<int:id>", views.get_produit, name='get_produit'),
    path("get_dc_autocompletion/<str:dc>", views.get_dc_autocompletion, name='get_dc_autocompletion'),
    path("get_dci_autocompletion/<str:dci>", views.get_dci_autocompletion, name='get_dci_autocompletion'),
    path("get_forme_autocompletion/<str:name>", views.get_forme_autocompletion, name='get_forme_autocompletion'),
    path("get_dosage_autocompletion/<str:name>", views.get_dosage_autocompletion, name='get_dosage_autocompletion'),
    path("get_presentation_autocompletion/<str:name>", views.get_presentation_autocompletion, name='get_presentation_autocompletion'),
]

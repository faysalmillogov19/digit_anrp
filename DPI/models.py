from django.db import models
from Produit.models import Categorie
from Demande.models import Demande,Nature_impression


class DPI(Demande):
    
    facture_proforma=models.TextField(null=True)
    code_facture=models.TextField(null=True)
    liste_colisage=models.TextField(null=True)
    certificat_atestation_don=models.TextField(null=True)
    total_item=models.IntegerField(null=True)
    nature_impression=models.ForeignKey(Nature_impression, null=True, on_delete=models.CASCADE)
    

    
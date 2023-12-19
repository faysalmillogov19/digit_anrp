from django.db import models
from Produit.models import Categorie
from Demande.models import Demande

class Nature_impression_asi(models.Model):
    libelle=models.CharField(max_length=25)

    class Meta:
        verbose_name = ("demandeur")
        verbose_name_plural = ("demandeurs")

class ASI(Demande):
    
    facture_proforma=models.TextField(null=True)
    certicat_bonne_pratique=models.TextField(null=True)
    certificat_analyse_prod=models.TextField(null=True)
    certificat_origine_prod=models.TextField(null=True)
    certificat_atestation_don=models.TextField(null=True)
    num_quittance=models.CharField(max_length=100,null=True)
    copie_quittance=models.TextField(null=True)
    nombre=models.IntegerField(null=True)
    cout=models.IntegerField(null=True)
    total_item=models.IntegerField(null=True)
    nature_impression=models.ForeignKey(Nature_impression_asi, null=True, on_delete=models.CASCADE)

    
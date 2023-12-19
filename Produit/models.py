from django.db import models
from Demande.models import Demande

class Categorie(models.Model):
    libelle=models.CharField(max_length=50)
    #description=models.CharField(max_length=100, null=True)

class Produit(models.Model):
    dc=models.CharField(max_length=250,null=True)
    dci=models.CharField(max_length=250,null=True)
    forme=models.CharField(max_length=50)
    dosage=models.IntegerField(null=True)
    presentation=models.TextField(null=True)
    classe_therapeutique=models.TextField(null=True)
    voie_administration=models.TextField(null=True)
    fabricant=models.TextField(null=True)
    titulaire_amm=models.TextField(null=True)
    code_amm=models.TextField(null=True)
    expiration_amm=models.DateField(null=True)
    pght=models.IntegerField(null=True)
    categorie=models.ForeignKey(Categorie, null=True, on_delete=models.CASCADE)

class Produit_demande(models.Model):
    dc=models.CharField(max_length=250,null=True)
    dci=models.CharField(max_length=250,null=True)
    forme=models.CharField(max_length=50)
    dosage=models.IntegerField(null=True)
    presentation=models.TextField(null=True)
    quantite=models.IntegerField(null=True)
    cout=models.IntegerField(null=True)
    categorie=models.ForeignKey(Categorie, null=True, on_delete=models.CASCADE)
    demande=models.ForeignKey(Demande, on_delete=models.CASCADE)
    amm=models.BooleanField(default=False)

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Demandeur(models.Model):
    tel=models.IntegerField(null=True)
    adresse=models.TextField(null=True)
    structure=models.CharField(max_length=150)
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
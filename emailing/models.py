from django.db import models
from Demande.models import Type_demande

class Protocole(models.Model):
	nom=models.CharField(max_length=25)

class EmailMessage(models.Model):
	objet=models.TextField(null=True)
	message=models.TextField(null=True)
	type_demande=models.ForeignKey(Type_demande, null=True, on_delete=models.CASCADE)
	modif_url=models.TextField(null=True)

class ServerConfiguration(models.Model):
	email = models.TextField()
	username= models.TextField(null=True)
	password= models.TextField(null=True)
	key= models.TextField(null=True)
	server_url= models.TextField(default="smtp.gmail.com")
	protocole=models.ForeignKey(Protocole, on_delete=models.CASCADE)
	port= models.IntegerField()
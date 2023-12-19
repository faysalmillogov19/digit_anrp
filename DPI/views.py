from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import DPI
from Demande.models import Demande, Type_expediteur, Voie_entree,Statut
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from Filing.views import uploadFile, deleteFile, generateQRCode, add_text_Recepice
import json
from datetime import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from SystemConf.Front_Control_Access import access_to_demande
from emailing.views import Send_mailFile
from emailing.models import EmailMessage


@login_required(login_url='demandeur_signin')
def add_produit(request, id_demande):

	if request.method=="POST":
		demandeur=Demandeur.objects.filter(user=request.user).first()
		element= Produit_demande()
		if id_demande==0:
			dpii=DPI()
			dpii.demandeur=demandeur
			dpii.save()
			element.demande=Demande.objects.get(id=dpii.id)
		else:
			element.demande=Demande.objects.get(id=id_demande)

		element.categorie=Categorie.objects.get( id=request.POST.get('categorie') )
		element.dc=request.POST.get('dc')
		element.dci=request.POST.get('dci')
		element.forme=request.POST.get('forme')
		element.dosage=request.POST.get('dosage')
		element.presentation=request.POST.get('presentation')
		element.quantite=request.POST.get('quantite')
		element.cout=request.POST.get('cout')
		element.save()
		return redirect('dpi_list_produit', id_demande=element.demande.id)
	else:
		categories=Categorie.objects.all()
		return render(request,'DPI/add_produit.html',{'categories':categories,'id_demande':id_demande})

@access_to_demande
def list_produit(request, id_demande):
	produits= Produit_demande.objects.filter(demande=id_demande)
	return render(request,'DPI/list_produit.html',{'produits':produits,'id_demande':id_demande})

@login_required(login_url='demandeur_signin')
def delete_produit(request, id):
	element=Produit_demande.objects.get(id=id)
	element.delete()
	return redirect('dpi_list_produit', id_demande=element.demande.id)

@login_required(login_url='demandeur_signin')
def set_produit(request, id):
	if request.method=='POST':
		element=Produit_demande.objects.get(id=id)
		element.categorie=Categorie.objects.get( id=request.POST.get('categorie') )
		element.dc=request.POST.get('dc')
		element.dci=request.POST.get('dci')
		element.forme=request.POST.get('forme')
		element.dosage=request.POST.get('dosage')
		element.presentation=request.POST.get('presentation')
		element.quantite=request.POST.get('quantite')
		element.cout=request.POST.get('cout')
		element.save()
		return redirect('dpi_list_produit', id_demande=element.demande.id)
	else:
		produit=Produit_demande.objects.get(id=id)
		categories=Categorie.objects.all()
		return render(request,'DPI/set_produit.html',{'categories':categories,'produit':produit})

@access_to_demande
def expediteur(request, id_demande):
	if request.method=="POST":
		element= DPI.objects.get(id=id_demande)
		element.type_expediteur=Type_expediteur.objects.get( id=request.POST.get('type_expediteur') )
		element.voie_entree=Voie_entree.objects.get( id=request.POST.get('voie') )
		element.nom_expediteur=request.POST.get('nom_expediteur')
		element.adresse_expediteur=request.POST.get('adresse_expediteur')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.save()
		return redirect('dpi_pieces_jointes', id_demande=element.id)
	else:
		type_expediteurs=Type_expediteur.objects.all()
		voies=Voie_entree.objects.all()
		element=DPI.objects.get(id=id_demande)
		return render(request,'DPI/add_expediteur.html',{'element':element,'id_demande':id_demande,'type_expediteurs':type_expediteurs,'voies':voies})

@access_to_demande
def pieces_jointes(request, id_demande):
	if request.method=="POST":
		element= DPI.objects.get(id=id_demande)
		if request.FILES.get("facture_proforma"):
			element.facture_proforma=uploadFile(request.FILES.get("facture_proforma"),"static/", "uploads/DPI/Proforma/", '.pdf')
		
		if request.FILES.get("certificat_atestation_don"):
			element.certificat_atestation_don=uploadFile(request.FILES.get("certificat_atestation_don"), "static/", "uploads/DPI/ATTESTATION_DON/", '.pdf')
		
		element.code_facture=request.POST.get("code_facture")
		
		element.save()
		return redirect('dpi_recap_dpi', id_demande=element.id)
	else:
		element=DPI.objects.get(id=id_demande)
		return render(request,'DPI/add_piece.html',{'element':element,'id_demande':id_demande})

@access_to_demande
def recap(request, id_demande):
	nombre=Produit_demande.objects.filter( demande=Demande.objects.get(id=id_demande)).count()
	dpii=DPI.objects.get(id=id_demande)
	
	if  (len(str(dpii.facture_proforma)) == 0 ) or (dpii.nom_expediteur is None) or (dpii.nom_transitaire is None) or (dpii.type_expediteur is None) :
		return render(request,'DPI/uncomplete.html',{'id_demande':id_demande})
	else:
		return render(request,'DPI/recap.html',{'nombre':nombre,'id_demande':id_demande})

@access_to_demande
def valid_demande(request, id_demande):
	if request.method=='POST':

		dpii=DPI.objects.get(id=id_demande)
		dpii.total_item=Produit_demande.objects.filter( demande=Demande.objects.get(id=id_demande) ).count()
		dpii.date_soumission=datetime.today()
		dpii.statut=Statut.objects.get(id=3)
		dpii.save()
		
		demandeur=Demandeur.objects.filter(user=request.user).first()
		
		code=str(dpii.date_soumission.strftime("%d%m%Y"))+str(dpii.id)

		data=[	
				"Déclaration Préalable d’Importation (DPI)",
				"Code: "+code,
				"Nom : "+demandeur.user.first_name,
				"Structure: "+demandeur.structure,
				"Téléphone: "+str(demandeur.tel),
				"Email: "+demandeur.user.email,
				"Total Produit: "+str(dpii.total_item),
				"Date: "+str(dpii.date_soumission.strftime("%d/%m/%Y"))
		]

		qr_code=generateQRCode("http://localhost:800/", 'static/uploads/Recepice/')
		filename=add_text_Recepice(data, qr_code)
		msg=EmailMessage.objects.get(id=3)
		send=Send_mailFile(msg.objet, msg.message, demandeur.user.email, filename)
		deleteFile(qr_code)
		

		return render(request,'end_demande.html',{})

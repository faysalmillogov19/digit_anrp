from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import ASI
from Demande.models import Demande, Type_expediteur, Voie_entree,Statut
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from Filing.views import uploadFile, deleteFile, generateQRCode, add_text_Recepice
import json
from datetime import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from SystemConf.Front_Control_Access import access_to_asi
from emailing.views import Send_mailFile
from emailing.models import EmailMessage


@login_required(login_url='demandeur_signin')
def add_produit(request, id_asi):
	if request.method=="POST":
		demandeur=Demandeur.objects.filter(user=request.user).first()
		element= Produit_demande()
		if id_asi==0:
			asi=ASI();
			asi.demandeur=demandeur
			asi.save()
			element.demande=Demande.objects.get(id=asi.id)
		else:
			element.demande=Demande.objects.get(id=id_asi)

		element.categorie=Categorie.objects.get( id=request.POST.get('categorie') )
		element.dc=request.POST.get('dc')
		element.dci=request.POST.get('dci')
		element.forme=request.POST.get('forme')
		element.dosage=request.POST.get('dosage')
		element.presentation=request.POST.get('presentation')
		element.quantite=request.POST.get('quantite')
		element.cout=request.POST.get('cout')
		element.amm=verify_amm(element.categorie, element.dc, element.dosage)
		element.save()
		return redirect('/asi/list_produit/'+str(element.demande.id))
	else:
		categories=Categorie.objects.all()
		return render(request,'ASI/add_produit.html',{'categories':categories,'id_asi':id_asi})

@access_to_asi
def list_produit(request, id_asi):
	produits= Produit_demande.objects.filter(demande=id_asi)
	return render(request,'ASI/list_produit.html',{'produits':produits,'id_asi':id_asi})

@login_required(login_url='demandeur_signin')
def delete_produit(request, id):
	element=Produit_demande.objects.get(id=id)
	element.delete()
	return redirect('/asi/list_produit/'+str(element.demande.id))

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
		element.amm=verify_amm(element.categorie, element.dc, element.dosage)
		element.save()
		return redirect('/asi/list_produit/'+str(element.demande.id))
	else:
		produit=Produit_demande.objects.get(id=id)
		categories=Categorie.objects.all()
		return render(request,'ASI/set_produit.html',{'categories':categories,'produit':produit})

@access_to_asi
def expediteur(request, id_asi):
	if request.method=="POST":
		element= ASI.objects.get(id=id_asi)
		element.type_expediteur=Type_expediteur.objects.get( id=request.POST.get('type_expediteur') )
		element.voie_entree=Voie_entree.objects.get( id=request.POST.get('voie') )
		element.nom_expediteur=request.POST.get('nom_expediteur')
		element.adresse_expediteur=request.POST.get('adresse_expediteur')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.save()
		return redirect('/asi/pieces_jointes/'+str(element.id))
	else:
		type_expediteurs=Type_expediteur.objects.all()
		voies=Voie_entree.objects.all()
		element=ASI.objects.get(id=id_asi)
		return render(request,'ASI/add_expediteur.html',{'element':element,'id_asi':id_asi,'type_expediteurs':type_expediteurs,'voies':voies})

@access_to_asi
def pieces_jointes(request, id_asi):
	if request.method=="POST":
		element= ASI.objects.get(id=id_asi)
		if request.FILES.get("facture_proforma"):
			element.facture_proforma=uploadFile(request.FILES.get("facture_proforma"),"static/", "uploads/ASI/Proforma/", '.pdf')
		if request.FILES.get("certicat_bonne_pratique"):
			element.certicat_bonne_pratique=uploadFile(request.FILES.get("certicat_bonne_pratique"), "static/", "uploads/ASI/BP/", '.pdf')
		if request.FILES.get("certificat_analyse_prod"):
			element.certificat_analyse_prod=uploadFile(request.FILES.get("certificat_analyse_prod"), "static/", "uploads/ASI/AP/", '.pdf')
		if request.FILES.get("certificat_origine_prod"):
			element.certificat_origine_prod=uploadFile(request.FILES.get("certificat_origine_prod"), "static/", "uploads/ASI/OP/", '.pdf')
		if request.FILES.get("certificat_atestation_don"):
			element.certificat_atestation_don=uploadFile(request.FILES.get("certificat_atestation_don"), "static/", "uploads/ASI/AD", '.pdf')
		element.save()
		return redirect('/asi/recap_asi/'+str(element.id))
	else:
		element=ASI.objects.get(id=id_asi)
		sans_amm=Produit_demande.objects.filter(amm=False).first()
		proforma_exist= len(str(element.facture_proforma)) == 0
		bp_exist= len(str(element.certicat_bonne_pratique)) == 0
		return render(request,'ASI/add_piece.html',{'element':element,'id_asi':id_asi,'sans_amm':sans_amm,'bp_exist':bp_exist,'proforma_exist':proforma_exist})

#@access_to_asi
def recap_asi(request, id_asi):
	nombre=Produit_demande.objects.filter( demande=Demande.objects.get(id=id_asi), amm=False ).count()
	cout=2000*nombre
	asi=ASI.objects.get(id=id_asi)
	complete=len(str(asi.certificat_atestation_don))
	if  (len(str(asi.facture_proforma)) == 0 ) or (len(str(asi.certicat_bonne_pratique)) == 0 ) or (asi.nom_expediteur is None) or (asi.nom_transitaire is None) or (asi.type_expediteur is None) :
		return render(request,'ASI/uncomplete_asi.html',{'id_asi':id_asi})
	else:
		return render(request,'ASI/recap_asi.html',{'nombre':nombre,'cout':cout,'id_asi':id_asi})

#@access_to_asi
def valid_asi(request, id_asi):
	if request.method=='POST':

		asi=ASI.objects.get(id=id_asi)
		asi.total_item=Produit_demande.objects.filter( demande=Demande.objects.get(id=id_asi) ).count()
		asi.date_soumission=datetime.today()

		
		demandeur=Demandeur.objects.filter(user=request.user).first()
		
		if int(request.POST.get('nombre')) > 0:
			asi.nombre=int(request.POST.get('nombre'))
			asi.cout=int(request.POST.get('cout'))
			asi.statut=Statut.objects.get(id=2)
			asi.save()
		else:
			asi.statut=Statut.objects.get(id=3)
			asi.nombre=0
			asi.cout=0
			asi.save()

		code=str(asi.date_soumission.strftime("%d%m%Y"))+str(asi.id)

		data=[	
				"Demande d’Autorisation Spécial d’Importation (ASI)",
				"Code: "+code,
				"Nom : "+demandeur.user.first_name,
				"Structure: "+demandeur.structure,
				"Téléphone: "+str(demandeur.tel),
				"Email: "+demandeur.user.email,
				"Total Produit: "+str(asi.total_item),
				"Produits sans AMM : "+str(asi.nombre),
				"Cout: "+str(asi.cout)+" F CFA",
				"Date: "+str(asi.date_soumission.strftime("%d/%m/%Y"))
		]

		qr_code=generateQRCode("http://localhost:800/", 'static/uploads/Recepice/')
		filename=add_text_Recepice(data,qr_code)
		msg=EmailMessage.objects.get(id=1)
		send=Send_mailFile(msg.objet, msg.message, demandeur.user.email, filename)
		deleteFile(qr_code)
		deleteFile(filename)

		return render(request,'end_demande.html',{})


##############################################################################################################
######################  FILTRAGE DES DIFFERENTTS CHAMPS AUTOCOMPLETION PRODUITS ##############################
##############################################################################################################

def get_produit(request, id):
	data=Produit.objects.filter(categorie=id)
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_dc_autocompletion(request, dc):
	data=Produit.objects.filter(dc__contains=dc.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_dci_autocompletion(request, dci):
	data=Produit.objects.filter(dci__contains=dci.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_forme_autocompletion(request, name):
	data=Produit.objects.filter(forme__contains=name)
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_dosage_autocompletion(request, name):
	data=Produit.objects.filter(dosage__contains=name.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_presentation_autocompletion(request, name):
	data=Produit.objects.filter(presentation__contains=name.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def verify_amm(categorie, dc, dosage):
	today=datetime.today()
	return Produit.objects.filter(categorie=categorie, dc__contains=dc, dosage__contains=dosage,expiration_amm__gte=today).exists()


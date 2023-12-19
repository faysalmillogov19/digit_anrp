from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import ADI
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
def add(request):

	if request.method=="POST":
		demandeur=Demandeur.objects.filter(user=request.user).first()
		element=ADI()
		element.demandeur=demandeur
		element.type_expediteur=Type_expediteur.objects.get( id=request.POST.get('type_expediteur') )
		element.voie_entree=Voie_entree.objects.get( id=request.POST.get('voie') )
		element.nom_expediteur=request.POST.get('nom_expediteur')
		element.adresse_expediteur=request.POST.get('adresse_expediteur')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')

		if request.FILES.get("facture_proforma"):
			element.facture_proforma=uploadFile(request.FILES.get("facture_proforma"),"static/", "uploads/ADI/Proforma/", '.pdf')
		
		element.code_facture=request.POST.get("code_facture")

		element.total_item=request.POST.get('nombre')
		element.date_soumission=datetime.today()
		element.statut=Statut.objects.get(id=3)
		element.save()

		code=str(element.date_soumission.strftime("%d%m%Y"))+str(element.id)

		data=[	
				"Demande d’Attestation Dérogatoire d’Importation (ADI)",
				"Code: "+code,
				"Nom : "+demandeur.user.first_name,
				"Structure: "+demandeur.structure,
				"Téléphone: "+str(demandeur.tel),
				"Email: "+demandeur.user.email,
				"Total Produit: "+str(element.total_item),
				"Date: "+str(element.date_soumission.strftime("%d/%m/%Y"))
		]

		qr_code=generateQRCode("http://localhost:800/", 'static/uploads/Recepice/')
		filename=add_text_Recepice(data,qr_code)
		msg=EmailMessage.objects.get(id=4)
		send=Send_mailFile(msg.objet, msg.message, demandeur.user.email, filename)
		deleteFile(qr_code)
		
		return render(request,'end_demande.html',{})

	else:
		type_expediteurs=Type_expediteur.objects.all()
		voies=Voie_entree.objects.all()
		return render(request,'ADI/add.html',{'type_expediteurs':type_expediteurs,'voies':voies})

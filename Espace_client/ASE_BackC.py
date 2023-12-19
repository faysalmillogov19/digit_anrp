from django.shortcuts import render,redirect
from ASE.models import ASE
from Demande.models import Demande, Type_expediteur, Voie_entree, Statut, Traitement, Nature_impression, Signataire
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from SystemConf.Back_Control_Access import access_to_demande
from emailing.views import Send_mailText, Send_mailFile
from emailing.models import EmailMessage
from django.db.models import Q



@access_to_demande
def list(request):
	user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
	user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
	user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()

	if user_is_sh:
		data=ASE.objects.filter(statut=3)
	elif user_is_dt:
		data=ASE.objects.filter(statut__gte=3, statut__lte=5)
	elif user_is_dg:
		data=ASE.objects.filter(statut__gt=5, statut__lte=7)
	else:
		data=ASE.objects.all()

	return render(request,'Espace_client/ase/list_ase.html',{'data':data})


@access_to_demande
def list_produit(request, id):
	user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
	user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
	user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()
	can_treat=False;
	can_print=False;

	datum=ASE.objects.get(id=id)
	categories=Categorie.objects.all()
	natures=Nature_impression.objects.all()

	
	if user_is_sh:
		statut=Statut.objects.filter(id=4)
		can_treat=True
	elif user_is_dt:
		statut=Statut.objects.filter(~Q(id=5), id__gte=3, id__lte=6)
		can_treat=True
		can_print=True
	elif user_is_dg:
		statut=Statut.objects.filter(id__gte=5, id__lte=7)
		can_print=True
	else:
		statut=Statut.objects.all()

	produits=Produit_demande.objects.filter(demande=Demande.objects.get(id=id))
	produit_amm=Produit.objects.all()
	return render(request,'Espace_client/ase/list_produit.html',{'datum':datum,'produits':produits,'statut':statut,'categories':categories,'produit_amm':produit_amm,"can_treat":can_treat,"can_print":can_print,'natures':natures})


def treat(request, id):
	if request.method=="POST":

		statut=Statut.objects.get(id=int(request.POST.get('statut')))

		ase=ASE.objects.get(id=id)
		ase.statut=statut
		if request.POST.get('nature'):
			ase.nature_impression=Nature_impression.objects.get(id=int(request.POST.get('nature')))
		
		ase.save()

		traitement=Traitement()
		traitement.type_demande=4
		traitement.demande=ase
		traitement.statut=statut
		traitement.commentaire=request.POST.get('commentaire')
		traitement.save()
	return redirect('list_ase')


def renvoie_modification(request):
	if request.method=="POST":
		
		id=request.POST.get('id')
		element=Demande.objects.get(id=int(id))
		element.statut=Statut.objects.get(id=1)
		element.save()

		url=EmailMessage.objects.get(id=2).modif_url
		email=element.demandeur.user.email
		objet=request.POST.get('objet')
		message=request.POST.get('message')+'\n Cliquer sur le lien: '+url+id
		Send_mailText(objet, message, email)
		return redirect('list_ase')



def print_ase(request, id):

	datum=ASE.objects.get(id=id)
	produits=Produit_demande.objects.filter(demande=Demande.objects.get(id=id))
	signataire=Signataire.objects.get(id=1)
	libelle_demande="Autorisation Spéciale d'Exportation(ASE)"
	intitule_demande="AUTORISATION SPECIALE D'EXPORTATION"

	if datum.nature_impression_id == 1:
		return render(request, "Espace_client/DEMANDE_print.html", {'datum':datum,'produits':produits,'signataire':signataire, 'libelle_demande':libelle_demande,'intitule_demande':intitule_demande} )
	elif datum.nature_impression_id == 2:
		return render(request, "Espace_client/REJET.html", {'datum':datum, 'signataire':signataire,'libelle_demande':libelle_demande} )

	return redirect('list_asi')


from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
import os
#from .models import ADI,DPI,ASI,ARI,ASE,Demande,Voie_entree,Specialisation,Demandeur

'''
def add_adi(request):
	if request.method=="POST":
		element= ADI()
		element.demandeur=Demandeur.objects.get(id=1);
		file_input=request.FILES.get("fichier")
		element.facture_proforma=uploadFile(file_input, "ADI/", '.pdf')
		element.save();
	else:
		return render(request,'Demande/add_adi.html',{})
	return redirect('/')


def add_dpi(request):
	if request.method=="POST":
		
		element=DPI()
		element.demandeur=Demandeur.objects.get(id=1);
		element.nom_fournisseur=request.POST.get('nom_fournisseur')
		element.adresse_fournisseur=request.POST.get('adresse_fournisseur')
		element.nom_fabricant=request.POST.get('nom_fabricant')
		element.adresse_fabricant=request.POST.get('adresse_fabricant')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.voie_entree=Voie_entree.objects.get(id=request.POST.get('voie')) 
		element.facture_proforma=uploadFile(request.FILES.get("proforma"), "DPI/", '.pdf')
		#element.amm=uploadFile(request.FILES.get("amm"), "uploads/DPI/amm/", '.pdf')
		element.save();
	else:
		voies=Voie_entree.objects.all()
		return render(request,'Demande/add_dpi.html',{'voies':voies})
	return redirect('/')

def add_ari(request):
	if request.method=="POST":
		
		element=ARI()
		element.demandeur=Demandeur.objects.get(id=1);
		element.nom_fournisseur=request.POST.get('nom_fournisseur')
		element.adresse_fournisseur=request.POST.get('adresse_fournisseur')
		element.nom_fabricant=request.POST.get('nom_fabricant')
		element.adresse_fabricant=request.POST.get('adresse_fabricant')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.voie_entree=Voie_entree.objects.get(id=request.POST.get('voie')) 
		element.facture_proforma=uploadFile(request.FILES.get("proforma"), "ARI/proforma/", '.pdf')
		element.autorisation=uploadFile(request.FILES.get("autorisation"), "/ARI/Autorisation/", '.pdf')
		element.save();
	else:
		voies=Voie_entree.objects.all()
		return render(request,'Demande/add_ari.html',{'voies':voies})
	return redirect('/')

def add_ase(request):
	if request.method=="POST":
		
		element=ASE()
		element.demandeur=Demandeur.objects.get(id=1);
		element.nom_fournisseur=request.POST.get('nom_fournisseur')
		element.adresse_fournisseur=request.POST.get('adresse_fournisseur')
		element.nom_fabricant=request.POST.get('nom_fabricant')
		element.adresse_fabricant=request.POST.get('adresse_fabricant')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.voie_entree=Voie_entree.objects.get(id=request.POST.get('voie')) 
		element.facture_proforma=uploadFile(request.FILES.get("proforma"), "ASE/proforma/", '.pdf')
		element.autorisation_pecial_importation=uploadFile(request.FILES.get("autorisation"), "ASE/Autorisation/", '.pdf')
		element.save();
	else:
		voies=Voie_entree.objects.all()
		return render(request,'Demande/add_ase.html',{'voies':voies})
	return redirect('/')

'''
def uploadFile(file_input, folder, extension):
	name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str(extension)
	file_name=folder+name
	if not os.path.exists(file_name):
		default_storage.save('media/'+file_name, file_input)
	print(name)
	return name #file_name

def deleteFile(link):
	os.remove('static/'+link)


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Demande.models import Demande, Type_expediteur, Voie_entree,Statut
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from Demande.views import uploadFile, deleteFile
import json
import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def access_to_asi(views_func):
	def wrapper_func(request, *args, **kwargs):

		unautorhized=False
		user_is_demandeur=request.user.groups.filter(name="DEMANDEUR").exists()

		if not request.user.is_authenticated:
			return redirect('demandeur_signin')
		elif not user_is_demandeur:
			unautorhized=True



		demande=Demande.objects.filter(id=kwargs['id_asi']).first()

		if demande is None:
			unautorhized=True
		elif demande.statut.id>1:
			unautorhized=True
		elif demande.demandeur.user != request.user:
			unautorhized=True

		if unautorhized:
			return render(request,'access_forbiden.html')
		else:
			return views_func(request, *args, **kwargs)

	return wrapper_func



def access_to_demande(views_func):
	def wrapper_func(request, *args, **kwargs):

		unautorhized=False
		user_is_demandeur=request.user.groups.filter(name="DEMANDEUR").exists()

		if not request.user.is_authenticated:
			return redirect('demandeur_signin')
		elif not user_is_demandeur:
			unautorhized=True



		demande=Demande.objects.filter(id=kwargs['id_demande']).first()

		if demande is None:
			unautorhized=True
		elif demande.statut.id>1:
			unautorhized=True

		if unautorhized:
			return render(request,'access_forbiden.html')
		else:
			return views_func(request, *args, **kwargs)

	return wrapper_func


def is_demandeur(views_func):
	def wrapper_func(request, *args, **kwargs):

		unautorhized=False
		user_is_demandeur=request.user.groups.filter(name="DEMANDEUR").exists()

		if not request.user.is_authenticated:
			return redirect('demandeur_signin')
		elif not user_is_demandeur:
			return render(request,'access_forbiden.html')
		else:
			return views_func(request, *args, **kwargs)

	return wrapper_func

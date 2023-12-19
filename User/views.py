from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from emailing.views import Send_mailFile, Send_mailText
from django.db.models import Q
from SystemConf.Back_Control_Access import is_admin
# Create your views here.


def signin(request):

	if request.method=="POST":

		email=request.POST.get('email')
		password=request.POST.get('password')

		user=authenticate(username=email, password=password)

		if user is not None:
			login(request, user)
			return redirect('espace_client')
		else:
			messages="Identifiants incorrectes !!!!"
			return render(request,'User/SignIn.html',{'email':email, 'password':password, 'messages':messages})
	else:
		return render(request,'User/SignIn.html')

@login_required(login_url="espace_client")
def signout(request):
	if request.method=="POST":
		logout(request)
	return redirect('user_signin')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.create_user(username=request.POST.get("username"), email=request.POST.get("email"), password=request.POST.get("password"))
			user.first_name=request.POST.get("nom")
			user.is_active=False
			user.save()
			message="Votre compte a bien été crée sur la plateforme en ligne de l'ANRP. \n Merci d'attendre l'atendre l'activation du compte. Si cela met du temps informé votre administrateur !!!!!"
			created=Send_mailText("Notification de création compte",message,user.email)
			login(request, user)

		except Exception as e:
			created=0
			data={
					'username':request.POST.get("username"), 
					'email':request.POST.get("email"), 
					'nom': request.POST.get("nom"),
					'password':request.POST.get("password"),
					'message':'Cet utilisateur existe déjà. '
				}

		if created:
			return render(request, 'waiting_page.html',{'message':message})
		else:
			return render(request,'User/SignUp.html',data)
		
	else:

		return render(request,'User/SignUp.html')

@is_admin
def list(request):
	data=User.objects.all()
	groupes=Group.objects.filter(~Q(name='DEMANDEUR'))
	return render(request,'User/list.html',{'data':data,'groupes':groupes})

@is_admin
def user_state(request):
	if request.method=="POST":
		user=User.objects.get( id=request.POST.get('id_utilisateur') )
		user.is_active=request.POST.get('state')
		user.save()
	return redirect('user_list')

@is_admin
def set_profil(request):
	if request.method=="POST":
		role=request.POST.get('role')
		user=User.objects.get( id=request.POST.get('id_utilisateur') )
		is_same_role=user.groups.filter(name=role).exists()
		if not  is_same_role:
			group=user.groups.first()
			if not (group is None):
				user.groups.remove(group)
			grp=Group.objects.get(id=role)
			user.groups.add(grp)
			user.save()

						
	return redirect('user_list')


def get_role(request, user_id):
	user=User.objects.get( id=int(user_id) )
	group=user.groups.first()
	if group is None:
		role = 'AUCUN'
	else:
		role=group.name
	return JsonResponse({'role':role})#HttpResponse(data, content_type='application/json')

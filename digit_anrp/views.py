from django.shortcuts import render,redirect
from datetime import datetime, timedelta

def index(request):
	return render(request,'home.html',{})


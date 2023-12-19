from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.files.storage import default_storage
import socket
import os
import qrcode
from PIL import Image
import random
from emailing.views import Send_mailFile

# Create your views here.

def test(request):
	qr_code=generateQRCode("http://localhost:800/timbre/", 'static/uploads/Recepice/')
	data=[	
			"Demande d’Autorisation Spécial d’Importation (ASI)",
			"Code : 0612202340",
			"Nom et Prénom : Ouédraogo Wilfried",
			"Structure : PHARMABU",
			"Téléphone : 00226 64 20 30 00",
			"Email : milfay19@gmail.com",
			"Total Produit : 5",
			"Produits sans AMM : 3",
			"Cout : 6000 F CFA",
			"Date : 06 / 12 / 2023"
	]
	filename=add_text_Recepice(data,qr_code)
	send=Send_mailFile("subject", "message", "milfay19@gmail.com", filename)
	deleteFile(qr_code)
	deleteFile(filename)
	return HttpResponse(send)

def generateQRCode(data,folder):
    qr = qrcode.QRCode(version = 1,
                   box_size = 5,
                   border = 5) 
    qr.add_data(data)
 
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'red',
                        back_color = 'white')
    img= qr.make_image()
    name=folder+str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+'.png'
    img.save(name)
    return name



def add_text_Recepice(input, img):
	file_name='static/uploads/Recepice/'+str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+'.pdf'
	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=letter)
	can.setFillColorRGB(0, 0, 0)
	can.setFont("Times-Roman", 12)
	#position=[9.4, 8.75, 8.46, 8.17, 7.88, 7.135, 6.89, 6.6, 5.8, 5.55, 5.26, 2.45]
	#base=800/12.2
	y=600
	i=0
	for txt in input:
		#y=position[i]*base 
		x=31
		if i==0:
			x=183
			i=1
		y-=30

		can.drawString(x, y, str(txt))

	
	can.drawImage(img, 315, 350, width=100, preserveAspectRatio=True, mask='auto')
	can.save()
	packet.seek(0)
	new_pdf = PdfReader(packet)
	existing_pdf = PdfReader(open('static/uploads/Recepice/Recepice_template.pdf', "rb"))
	output = PdfWriter()
	page = existing_pdf.pages[0]
	page.merge_page(new_pdf.pages[0])
	output.add_page(page)
	outputStream = open(file_name, "wb")
	output.write(outputStream)
	outputStream.close()
	return file_name

def uploadFile(file_input, S_path,folder, extension):
	name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str(extension)
	file_name=S_path+folder+name
	if not os.path.exists(file_name):
		default_storage.save(file_name, file_input)
	print(file_name)
	print(folder+name)
	return folder+name #file_name


def deleteFile(link):
	exist=os.path.exists(link)
	if exist:
		os.remove(link)
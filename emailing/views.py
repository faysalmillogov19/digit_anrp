from django.shortcuts import render,redirect
from django.http import HttpResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from .models import ServerConfiguration, Protocole
import cryptocode, ssl
import string,random
from SystemConf.Back_Control_Access import is_admin

@is_admin
def Serverconfiguration(request):
	config=ServerConfiguration.objects.first()
	if config is None:
		config=ServerConfiguration()

	if request.POST:
		config.email=request.POST.get("email")
		config.username=request.POST.get("username")
		config.key=get_random_string(20)
		config.password=cryptocode.encrypt(request.POST.get("password"), config.key)
		config.server_url=request.POST.get("server_url")
		config.protocole=Protocole.objects.get(id=int( request.POST.get("protocole") ) ) 
		config.port=request.POST.get("port")
		config.save()
		return redirect('config_email')
	else:
		protocoles=Protocole.objects.all()
		return render(request, 'Espace_client/Emailing/config.html',{"protocoles":protocoles,'config':config})
	return ServerconfigurationForm(request)


# Create your views here.
def Send_mailFile(subject, message, destinataire, filename):
	try:
		config= ServerConfiguration.objects.first()
		monMail=config.email
		monPassword=cryptocode.decrypt(config.password, config.key)
		smtpserver=config.server_url
		port=config.port
		server=smtplib.SMTP(smtpserver,port)
		server.ehlo()
		server.starttls()
		server.login(monMail,monPassword)
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject		#f"Subject: {subject}\n{message}"
		msg['From'] = monMail
		msg['To'] = destinataire
		msg.attach(MIMEText(message.encode('utf-8'), _charset='utf-8'))		
		part = MIMEBase('application', 'octate-stream')
		part.set_payload(open(filename, 'rb').read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename='+filename)
		msg.attach(part)
		#server.sendmail(monMail,destinataire,msg.as_string())
		server.sendmail(monMail,destinataire,msg.as_string())
		i= 1
	except:
		i= 0
	return i

def Send_mailText(subject, message, toaddr):
	config= ServerConfiguration.objects.first()
	monMail=config.email
	monPassword=cryptocode.decrypt(config.password, config.key)
	smtp_server=config.server_url
	port=config.port

	i=0
	context = ssl.create_default_context()
	try:
		server = smtplib.SMTP(smtp_server,port)
		server.starttls(context=context)
		server.login(monMail, monPassword)
		msg = MIMEText(message.encode('utf-8'), _charset='utf-8')
		msg['Subject'] = subject	#f"Subject: {subject}\n{message}"
		msg['From'] = monMail
		msg['To'] = toaddr
		server.sendmail(monMail, toaddr, msg.as_string())
		i=1
	except Exception as exep:
		i=0
	finally:
		server.quit()
	return 1



def test(request):
	#r=Send_mailFile('Soumission du fichier', 'Hello bonjour tout le monde !!!!!', 'milfay19@gmail.com',"static/test.pdf")
	msg="Bonjour"
	subject="Ceci est un test"
	url="http://localhost:8000/demandeur/signin/"
	message="Toujours"+"\n"+url
	r=Send_mailText(subject, message, 'milfay19@gmail.com')
	return HttpResponse(r)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
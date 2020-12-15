# -*- coding: utf-8 -*-
#encoding:utf-8

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #el formulario de autenticación de django
from django.contrib.auth import authenticate, get_user_model, login,logout  #todas son por defecto
from django.contrib.auth.models import User  #django para crear usuarios
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import FormView #la vista genérica FormView
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator, InvalidPage, EmptyPage #imports para la paginacion
from django.core.mail import EmailMessage
from ajedrez_app.models import *  
from .forms import UserLoginForm, SignupForm #RegisterForm
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.conf import settings 
from django.urls import reverse_lazy 
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage #imports para la paginacion
from django.core.paginator import PageNotAnInteger  
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from stockfish import Stockfish
import json
from django.core import serializers
from django.contrib.syndication.views import Feed #RSS
import feedparser
from django.views.decorators.csrf import csrf_exempt 

		
#indicamos a la vista que no verifique el token csrf con el decorador
#@csrf_exempt 	
def home(request):
	
	actual=request.user   #usuario actual
	idusuario=0
	idusuario=actual.id 
	print ("\n\n=====INICIO HOME=========================")
	print ("Usuario Actual == "+str(actual))
	print ("idusuario:::"+str(idusuario))
	print ("autenticado=="+str(request.user.is_authenticated))
	print ("is_active=="+str(request.user.is_active))
	
	contrincante1=str(User.objects.get(id=4))
	contrincante2=str(User.objects.get(id=5))
	contrincante3=str(User.objects.get(id=6))
	
	jugador1=str(User.objects.get(id=1))
	jugador2=str(User.objects.get(id=2))
	jugador3=str(User.objects.get(id=3))
	
	ganadas=0
	perdidas=0
	empatadas=0
	elo=0
	total=0
	federacion=""
	quitartableros=0
	numconectados=0
	numpartidas=0
	
	#mostrar la lista de jugadores de la página principal
	usuarios = User.objects.all().order_by('id')
	print ("Usuarios")	
	for r in usuarios:
		print (str(r.id)+"     "+str(r.username))	
	print ("===============================")	
	
	print ("Jugadores")	
	print ("idjugador        Jugador   idusuario")	
	listajugadores = Jugador.objects.all().order_by('id')
	try:
		for r in listajugadores:
			print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
			if r.conectado==True:
				numconectados=numconectados+1
	except:
		print("Error al leer jugadores")
		
	if actual=="AnonymousUser":
		print ("entra como usuario anónimo")
		
	if idusuario!=None: 
		print ("==entra cuando SI existe ="+str(idusuario))
		try:
			jugador=Jugador.objects.get(user=idusuario) #usuario current por defecto si no existe uno concreto
		except:
			#en caso de que de error que coja un usuario por defecto
			jugador=Jugador.objects.get(user=1) #usuario current por defecto si no existe uno concreto
		
		idjugador=jugador.id
		ganadas=jugador.ganadas
		perdidas=jugador.perdidas
		empatadas=jugador.empatadas
		elo=jugador.elo
		federacion=jugador.federacion
		total=ganadas+perdidas+empatadas
		
		print ("\ntotales partidas del jugador:::::"+str(total))
		print ("==federacion="+str(jugador.federacion))
		print ("==idjugador="+str(idjugador))
		print ("==CONECTADO ANTES DE ="+str(jugador.conectado))
		
		#cuando un jugador entrar en el sitio web y se loguea actualiza en la tabla el campo conectado a true
		#equivale a hacer un update de sql
		jugadoraux=Jugador.objects.get(id=idjugador) 
		jugadoraux.conectado=True
		jugadoraux.save()
		
		print ("==CONECTADO DESPUES="+str(jugadoraux.conectado))
		print ("==OK=")
		request.session['actual']=str(actual) # almacenar en una variable de sesión el jugador actual tipo cookie en ram
	
		usuarios=Jugador.objects.filter(conectado=True).order_by('-elo') #descendente -  ascendente no poner signo
	
		#la paginacion
		page = request.GET.get('page')
		print ("pagina="+str(page))
		paginator = Paginator(usuarios, 10) 
		if page == None:
			page=paginator.num_pages
			page=1
		try:
			usuarios=paginator.get_page(page)
		except PageNotAnInteger:
			usuarios = paginator.page(1)
		except EmptyPage:
			usuarios = paginator.page(paginator.num_pages)
			
	
	print("Jugadores conectados::::::::::::::::::::::::"+str(numconectados))
	print ("Partidas")	
	partidas = Partida.objects.all().order_by('id')
	try:
		for r in partidas:
			print (str(r.id)+" "+str(r.user.username)+"  "+str(r.num_partida)+ "   "+str(r.estado))	
			if r.estado=='C':
				numpartidas=numpartidas+1
	except:
		print("Error al leer partidas")		
			
	room_name="publica" #la sala de chat pública del ajedrez
	
	context = { 'usuarios': usuarios,'ganadas': ganadas,'perdidas':perdidas,
	'empatadas':empatadas, 'elo':elo, 'total':total, 'jugador1':jugador1,'jugador2':jugador2,'jugador3':jugador3,
	'contrincante1':contrincante1,'contrincante2':contrincante2,'contrincante3':contrincante3, 'actual':actual, 
	'quitartableros':quitartableros,'federacion':federacion,'room_name': room_name,'numconectados':numconectados,'numpartidas':numpartidas}
	return render(request, 'home.html', context=context)
	
def about(request):
	return render(request, 'about.html')
	
def contact(request):
	return render(request, 'contact.html')
	
def configurar(request):
	return render(request, 'configurar.html')

def contrincante(request):
	welo=0
	welo1=0
	if request.GET.get('elo'):
		welo = request.GET.get('elo')	
		print("elo***************="+str(elo))
	if request.GET.get('elo1'):
		welo1 = request.GET.get('elo1')		
		print("elo1********************"+str(elo1))
	
	usuariocurrent=str(request.user)
	contrincante=""
	print("ACTUAL=["+str(usuariocurrent)+"]")
	
	username=request.user.username
	idusuario=request.user.id
	print("ojooooooo  "+username+"id="+str(idusuario))
	jugador=Jugador.objects.get(user=idusuario) 

	
	#print("user=["+str(user)+"]")
	usuarios=Jugador.objects.filter(conectado=True).filter(esperaoponente=True).exclude(user_id=idusuario).order_by('-elo') #descendente con  - , ascendente es sin signo (filter AND)
	
	for r in usuarios:
		#request.session['contrincantes']=str(r.user.username)
		contrincante=str(r.user.username)
		request.session['contrincante']=str(r.user.username)
		print("................>>>>>> CONTRINCANTE dentro del bucle "+str(contrincante))
	print("................>>>>>> CONTRINCANTE fuera del bucle "+str(contrincante))
	
	#la paginacion
	page = request.GET.get('page')
	print ("pagina="+str(page))
	paginator = Paginator(usuarios, 10) 
	if page == None:
		page=paginator.num_pages
		page=1
	try:
		usuarios=paginator.get_page(page)
	except PageNotAnInteger:
		usuarios = paginator.page(1)
	except EmptyPage:
		usuarios = paginator.page(paginator.num_pages)
	
	return render(request, 'contrincante.html', {'usuarios':usuarios,'usuariocurrent':usuariocurrent,'contrincante':contrincante})	

def filtrocontrincante(request,template_name='contrincante.html'):
	print("ENTRAAAA")
	welo=0
	welo1=0
	if request.POST.get('elo'):    #if request.GET.get('elo'):
		welo = request.POST.get('elo')	
		print("elo POST***************="+str(welo))
	if request.POST.get('elo1'):
		welo1 = request.POST.get('elo1')		
		print("elo1 POST********************"+str(welo1))
	
	username=request.user.username
	idusuario=request.user.id
	print("ojooooooo  "+username+"id="+str(idusuario))
	jugador=Jugador.objects.get(user=idusuario) 	
	
	usuarios=Jugador.objects.filter(conectado=True).filter(esperaoponente=True).filter(elo__gte=welo,elo__lte=welo1).exclude(user_id=idusuario).order_by('-elo') #descendente -  ascendente no poner signo
	
	contrincante=""
	for r in usuarios:
		#request.session['contrincantes']=str(r.user.username)
		contrincante=str(r.user.username)
		print("................>>>>>> CONTRINCANTE dentro del bucle "+str(contrincante))
	print("................>>>>>> CONTRINCANTE fuera del bucle "+str(contrincante))
	
	#la paginacion
	page = request.GET.get('page')
	print ("pagina en filtro="+str(page))
	paginator = Paginator(usuarios, 10) 
	if page == None:
		page=paginator.num_pages
		page=1
	try:
		usuarios=paginator.get_page(page)
	except PageNotAnInteger:
		usuarios = paginator.page(1)
	except EmptyPage:
		usuarios = paginator.page(paginator.num_pages)
	
	usuariocurrent=str(request.user)
	
	return render(request, 'contrincante.html', {'usuarios':usuarios,'usuariocurrent':usuariocurrent,'contrincante':contrincante})	

	
def jugar(request):
	print('DIRECTORIO BASE_DIR para ESTATICO: '+str(settings.BASE_DIR))
	print('DIRECTORIO ROOT para ESTATICO: '+str(settings.STATIC_ROOT))
	print("DATOS EN JUGAR");
	
	contrincante=""

	if 'elo' in request.session:
		print("ELO2...."+str(request.session['elo']))	 
	else:
		request.session['elo']=1000
		
	if 'contrincante' in request.session:	
		contrincante=str(request.session['contrincante'])
		print("contrincante...."+str(contrincante))
	if 'fichas' in request.session:		
		print("fichas...."+str(request.session['fichas']))
	else:
		request.session['fichas']='blancas'
	if 'partida' in request.session:		
		print("partida...."+str(request.session['partida']))
	else:
		request.session['partida']="publica"
	if 'tiempo' in request.session:			
		print("tiempo...."+str(request.session['tiempo']))
	else:
		request.session['tiempo']="no"
	if 'estado' in request.session:			
		print("estado...."+str(request.session['estado']))
	else:
		request.session['estado']=''
	if 'minutos' in request.session:		
		print("minutos...."+str(request.session['minutos']))
	else:
		request.session['minutos']="60"
	print("REQUEST...."+str(request.path))
	
	minutos=0
	tiempo=""
	
	tiempo=str(request.session['tiempo'])
	if tiempo=="si":
		minutos=request.session['minutos']
	else:
		minutos=0
	
	#comunicaciones con el posible contrincante
	nombre=""
	fen=""
	request.path_info="/static/img/chesspieces/wikipedia/"
	activarjuego=1
	context = {'usuarios': Jugador.objects.all(),'contrincante': contrincante,
	'elo':str(request.session['elo']),'partida':str(request.session['partida']),'tiempo':str(request.session['tiempo']),
	'estado':str(request.session['estado']),'minutos':str(request.session['minutos']),'activarjuego':activarjuego, 'fen':fen}
	return render(request, 'jugar.html', context)	
	
	
def configuracion(request):
	print('DIRECTORIO BASE_DIR para ESTATICO: '+str(settings.BASE_DIR))
	print('DIRECTORIO ROOT para ESTATICO: '+str(settings.STATIC_ROOT))
	#return render(request, 'jugar_original.html')
	#return render(request, 'jugar.html')
	print("DATOS EN JUGAR");
	
	#OJO ANULADAS HOY 18/10/2020
	print("ELO2...."+str(request.session['elo']))	
	#print("contrincantes...."+str(request.session['contrincantes']))
	print("fichas...."+str(request.session['fichas']))
	print("partida...."+str(request.session['partida']))
	print("tiempo...."+str(request.session['tiempo']))
	print("estado...."+str(request.session['estado']))
	print("minutos...."+str(request.session['minutos']))
	print("REQUEST...."+str(request.path))
	
	minutos=0
	tiempo=""
	
	tiempo=str(request.session['tiempo'])
	if tiempo=="si":
		minutos=request.session['minutos']
	else:
		minutos=0
	
	#comunicaciones con el posible contrincante
	'''
	nombre=""
	fen=""
	if request.is_ajax():
		if request.POST:
			print("\n\n ======== AJAX ENTRA POST 2====================");
			if request.POST.get('fen'):
				fen = request.POST.get('fen') #table es una variable de javascript
				print("fen==============="+str(fen))
			if request.POST.get('nombre'):
				nombre = request.POST.get('nombre') #table es una variable de javascript
				print("nombre==============="+str(nombre))	
			#return HttpResponse(json.dumps(data), content_type='application/json')
			#return JsonResponse(data)
		if request.GET:	
			print("\n\n ======== AJAX ENTRA GET 2====================");
	'''		
	
	request.path_info="/static/img/chesspieces/wikipedia/"
	
	contrincantes=str(request.session['contrincantes'])
	print("contrincantes en configuracion...."+str('contrincantes'))
	
	context = {'usuarios': Jugador.objects.all(),'contrincante': contrincantes,
	'elo':str(request.session['elo']),'partida':str(request.session['partida']),'tiempo':str(request.session['tiempo']),
	'estado':str(request.session['estado']),'minutos':str(request.session['minutos'])}
	return render(request, 'configuracion.html', context)		
	
#jugar contra la máquina
def jugar1(request):
	#nombre=str(User.objects.get(id=1))
	nombre=request.session['actual']
	print("nombre jugador="+str(nombre))
	if request.method=='POST':
		print("POST");
	if request.method=='GET':
		print("GET");
	return render(request, 'jugarmaquina.html', {'nombre':nombre})
	
def foro(request):
	return render(request, 'foro.html')

def noticias(request):
	return render(request, 'noticias.html')

def ranking(request):
	#context = {'usuarios': Jugador.objects.all()}
	#return render(request, 'ranking.html', context)
	#usuarios=Jugador.objects.filter(conectado=True).order_by('-elo') #descendente
	usuarios=Jugador.objects.all().order_by('-elo')[:10] #descendente muestra los 10 primeros registros
	return render(request, 'ranking.html', {'usuarios':usuarios})
	
def practicar(request):
	return render(request, 'practicar.html')
	
def busqueda(request):	
	return render(request, 'busqueda.html')	
	context = {'jugadores': Jugador.objects.all()}
	return render(request, 'busqueda.html', context)
	
def solicitudes(request):
	#print('DIRECTORIO BASE_DIR para ESTATICO: '+str(settings.BASE_DIR))
	#print("DATOS EN JUGAR");
	#print("ELO2...."+str(request.session['elo']))	
	#context = {'usuarios': Jugador.objects.all(),'contrincante': str(request.session['contrincantes']),
	#'elo':str(request.session['elo']),'partida':str(request.session['partida']),'tiempo':str(request.session['tiempo']),
	#'estado':str(request.session['estado'])}
	print ("--------SOLICITUDES---------------")	
	print ("--------Jugadores---------------")	
	print ("idjugador        Jugador   idusuario	conectado")	
	listajugadores = Jugador.objects.all().order_by('id')
	for r in listajugadores:
		print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
	
	#SOLICITUDES
	'''
	id = models.AutoField(primary_key=True)
	fecha_inicio = models.DateField("Fecha_Inicio",null=True,blank=True)
	duracion=models.IntegerField()  # en segundos de la solicitud
	ahora=models.DateTimeField()
	aceptada=models.BooleanField()
	cancelada=models.BooleanField()
	jugador1 = models.ForeignKey(Jugador, related_name='solicita',null=True, blank=True,on_delete=models.PROTECT) #Realiza la petición o solicitud
	jugador2 = models.ForeignKey(Jugador, related_name='responde',null=True, blank=True,on_delete=models.PROTECT) #recibe/responde a la petición o solicitud
	partida=models.ForeignKey(Partida,related_name='partida',null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	'''
	context = {'usuarios': Jugador.objects.filter(conectado=True)}
	return render(request, 'solicitudes.html', context)	
	
def enjuego(request):
	#print('DIRECTORIO BASE_DIR para ESTATICO: '+str(settings.BASE_DIR))
	#print("DATOS EN JUGAR");
	#print("ELO2...."+str(request.session['elo']))	
	#context = {'usuarios': Jugador.objects.all(),'contrincante': str(request.session['contrincantes']),
	#'elo':str(request.session['elo']),'partida':str(request.session['partida']),'tiempo':str(request.session['tiempo']),
	#'estado':str(request.session['estado'])}
	context = {'usuarios': Jugador.objects.all()}
	return render(request, 'partidasenjuego.html', context)	
	
def index(request):
	print("INDEX OJO")
	context = {
		'usuarios': User.objects
		if request.user.is_authenticated else []
    }
	return render(request, 'index.html', context)	
	
def cerrar(request):
	username = request.user.username
	password = request.user.password
	idusuario=request.user.id
	print("ojooooooo logout "+username+ "clave="+str(password)+"id="+str(idusuario))
	user = authenticate(request, username=username, password=password)
	
	jugador=Jugador.objects.get(user=idusuario) #usuario current por defecto si no existe uno concreto
	print ("==idjugador="+str(idusuario))
	jugador.conectado=False
	jugador.esperaoponente=False
	jugador.save()
	print ("==CONECTADO DESPUES="+str(jugador.conectado))
	
	#desconectamos al usuario
	logout(request)
	return redirect('/')	
	
		
###############################
# REGISTRO DE NUEVOS USUARIOS
###############################
def signup(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST) #form= SignupForm(request.POST)
		if form.is_valid():
			request.user.is_active = True
			request.user.is_staff = False
			request.user.is_superuser = False
			request.session['usuario']=request.POST.get('username') # MUY BIEEN aqui pilla bien el usuario registrado
			print('USUARIO DE SESION ='+str(request.session['usuario']))
			request.session['password']=request.POST.get('password_one') 
			print('PASSWORD DE SESION ='+str(request.session['password']))
			form.save(commit=True)
			
			try:
				usuarionuevo = Jugador()
				#usuarionuevo.User_id=4
				usuarionuevo.Federacion_id=3
				usuarionuevo.conectado=True
				usuarionuevo.elo=800
				usuarionuevo.ganadas=0
				usuarionuevo.perdidas =0
				usuarionuevo.empatadas = 0
				usuarionuevo.numfederado = 122
				usuarionuevo.anyosexperiencia=1
				usuarionuevo.save()
				print ("registro guardado OK")	
			except:	
				print("Error al guardar el nuevo jugador")

			'''
			directorio = "/temp"
			try:
				os.stat(directorio)
				print("el directorion existe")
			except:
				os.mkdir(directorio)
				print("creando el directorio")
			
			archivo = open("/temp/reservas.txt","w")
			registro=request.session['usuario']
			archivo.write(registro)
			archivo.close()
			'''
			return redirect('home')
	else:
		form= UserCreationForm()
		print("ELSE entra la primera vez al cargar el formulario de registro de usuarios signup")
	return render(request, 'signup.html', {'form': form})
		
#activa el email comprobando si el token es válido y entonces se inicia la sesión user.is_active=True
def activate(request, uidb64, token):
    print("uidb64="+str(uidb64))
    print("token="+str(token))
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(str(uid))
        #uid=uid.decode('utf-8') #ojo nueva la he incluido 
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print(str(token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        print(str(user))
        login(request, user)
        # return redirect('home')
        return HttpResponse('Gracias por la confirmación del email. Ahora ya puede acceder con su cuenta.')
    else:
        return HttpResponse('El enlace de Activación no es valido!')
		
			
def game_over(request):
    if request.is_ajax():
        try:
            board_pk = int(request.POST['board'])
            moves = list(map(int, request.POST['move_list'].split(',')))
        except KeyError:
            return HttpResponse('Error') # incorrect post
        # calcular la puntuación
        return HttpResponse(str(score))
    else:
        raise Http404	
		
def iniciarjuego(request):
	print ("==========>>>>>>>INICIARJUEGO")	
	'''
	listajugadores = Jugador.objects.all().order_by('id')
	for r in listajugadores:
		r.conectado=False
		esperaoponente=False
		r.save()
		print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
	'''
	 
	if request.method == 'POST':
		print ("\n\n\n==========>>>>>>>POST DE INICIARJUEGO")	
		request.session['elo']=request.POST.get('elo')
		request.session['contrincantes']=request.POST.get('contrincantes')
		print ("==========>>>>>>>CONTRINCANTES "+str(request.session['contrincantes']))	
		request.session['fichas']=request.POST.get('fichas')
		request.session['partida']=request.POST.get('partida')
		request.session['tiempo']=request.POST.get('tiempo')
		request.session['estado']="en espera"
		
		if request.session['tiempo']=="si":
			request.session['minutos']=request.POST.get('minutos')
		else:	
			request.session['minutos']="0"
			
		username = request.user.username
		password = request.user.password
		idusuario=request.user.id
		print("ojooooooo logout "+username+"id="+str(idusuario))
		jugador=Jugador.objects.get(user=idusuario) #usuario current por defecto si no existe uno concreto
		print ("==idjugador="+str(idusuario))
		jugador.esperaoponente=True
		jugador.save()
		print ("==espera oponente DESPUES="+str(jugador.esperaoponente))	
	
		#print("ELO...."+str(request.session['elo']))	
		#print("contrincantes...."+str(request.session['contrincantes']))
		#print("fichas...."+str(request.session['fichas']))
		#print("partida...."+str(request.session['partida']))
		#print("tiempo...."+str(request.session['tiempo']))
		#print("estado...."+str(request.session['estado']))
	
		#context = {'usuarios': Jugador.objects.all()}
		#return render(request, 'jugar.html', context)			
	#return jugar(request) #es lo mismo que las 2 lineas de arriba
	if request.method == 'GET':
		print ("==========>>>>>>>GET DE INICIARJUEGO")	
		#request.session['contrincantes']=request.POST.get('contrincantes')
		print ("==========>>>>>>>GET DE INICIARJUEGO "+str(request.session['contrincantes']))	
		username = request.user.username
		password = request.user.password
		idusuario=request.user.id
		print("ojooooooo logout "+username+ "clave="+str(password)+"id="+str(idusuario))
		jugador=Jugador.objects.get(user=idusuario) #usuario current por defecto si no existe uno concreto
		print ("==idjugador="+str(idusuario))
		jugador.esperaoponente=True
		jugador.save()
		print ("==espera oponente DESPUES="+str(jugador.esperaoponente))
	
	return configuracion(request) 

def stream(request):
    def event_stream():
        while True:
            time.sleep(3)
            yield 'data: Hora del Servidor: %s\n\n' % datetime.datetime.now()
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
	
def stockFish_init(request):
	stockfish = Stockfish(parameters={"Threads": 2, "Minimum Thinking Time": 30})
	stockfish.set_position(["e2e4", "e7e6"])
	#posición de Forsyth–Edwards Notation (FEN)
	stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
	#coge el mejor movimiento
	stockfish.get_best_move()   #stockfish.get_best_move_time(1000) en base al tiempo
	#nivel del motor
	stockfish.set_skill_level(15)
	#parámetros por defecto
	stockfish.get_parameters()
	#coge la posición FEN
	stockfish.get_fen_position()
	#coge el tablero por defecto del usuario
	stockfish.get_board_visual()
	#evalua jugada
	stockfish.get_evaluation()
	p = subprocess.Popen('stockfish-x64.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	p.stdin.write("position startpos moves e2e4 e7e5\n")
	p.stdin.write("go infinite\n")
	p.stdin.flush()
	time.sleep(1)
	print(p.communicate())

def get(request):
	respuesta = {'ajax_respuesta':request}
	datos = json.dumps(respuesta)
	request.response.headers.add_header('content-type', 'application/json', charset='utf-8')
	request.response.out.write(datos)
	   
def movimientoStockfish(request):
	resultados = {}
	games_shallow_win_or_draw={}
	for depth_var in range(5,10):
		for i in range(5):
			engines = {
			'shallow': Engine(depth=depth_var, rand=False),
			'deep': Engine(depth=10, rand=False),
			}
			m = Match(engines=engines)
			winner = m.run()
			if winner == 'deep':
				resultados[depth_var]=resultados.get(depth_var,0)+1
			elif winner == None:
				resultados[depth_var]=resultados.get(depth_var,0)+0.5
				print("draw", "white: %s \n" % m.white, movelisttostr(m.moves))
			else:
				print('shallow', "white: %s \n" % m.white, movelisttostr(m.moves))
		print(i)
	print(resultados)
	
def desconectarActual(request):
	actual=request.user   #usuario actual
	idusuario=0
	idusuario=actual.id 
	print ("\n\n===== DESCONECTAR =========================")
	print ("Usuario Actual == "+str(actual))
	print ("idusuario:::"+str(idusuario))
	print ("autenticado=="+str(request.user.is_authenticated))
	print ("is_active=="+str(request.user.is_active))
	
	usuario=User.objects.get(id=idusuario)
	usuario.conectado=False
	usuario.save()
	print ("==========>>>>>>>registro actualizado OK")	
	#return render(request, 'about.html')
	return HttpResponseRedirect('http://localhost:8000')
	
def desconectar(request):
	print ("--------Jugadores---------------")	
	print ("idjugador        Jugador   idusuario	conectado")	
	listajugadores = Jugador.objects.all().order_by('id')
	for r in listajugadores:
		r.conectado=False
		esperaoponente=False
		r.save()
		print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
	print ("==========>>>>>>>registros actualizados OK")	
	
	actual=request.user   #usuario actual
	idusuario=0
	idusuario=actual.id 
	print ("\n\n=====INICIO HOME=========================")
	print ("Usuario Actual == "+str(actual))
	print ("idusuario:::"+str(idusuario))
	print ("autenticado=="+str(request.user.is_authenticated))
	print ("is_active=="+str(request.user.is_active))
	
	contrincante1=str(User.objects.get(id=4))
	contrincante2=str(User.objects.get(id=5))
	contrincante3=str(User.objects.get(id=6))
	
	jugador1=str(User.objects.get(id=1))
	jugador2=str(User.objects.get(id=2))
	jugador3=str(User.objects.get(id=3))
	
	ganadas=0
	perdidas=0
	empatadas=0
	elo=0
	total=0
	federacion=""
	quitartableros=0
	numconectados=0
	
	#mostrar la lista de jugadores de la página principal
	usuarios = User.objects.all().order_by('id')
	print ("Usuarios")	
	for r in usuarios:
		print (str(r.id)+"     "+str(r.username))	
	print ("===============================")	
	
	print ("Jugadores")	
	print ("idjugador        Jugador   idusuario")	
	listajugadores = Jugador.objects.all().order_by('id')
	try:
		for r in listajugadores:
			print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
			if r.conectado==True:
				numconectados=numconectados+1
	except:
		print("Error al leer jugadores")
		
	if actual=="AnonymousUser":
		print ("entra como usuario anónimo")
		
	if idusuario!=None: 
		print ("==entra cuando SI existe ="+str(idusuario))
		try:
			jugador=Jugador.objects.get(user=idusuario) #usuario current por defecto si no existe uno concreto
		except:
			#en caso de que de error que coja un usuario por defecto
			jugador=Jugador.objects.get(user=1) #usuario current por defecto si no existe uno concreto
		
		idjugador=jugador.id
		ganadas=jugador.ganadas
		perdidas=jugador.perdidas
		empatadas=jugador.empatadas
		elo=jugador.elo
		federacion=jugador.federacion
		total=ganadas+perdidas+empatadas
		
		print ("\ntotales partidas del jugador:::::"+str(total))
		print ("==federacion="+str(jugador.federacion))
		print ("==idjugador="+str(idjugador))
		print ("==CONECTADO ANTES DE ="+str(jugador.conectado))
		
		#cuando un jugador entrar en el sitio web y se loguea actualiza en la tabla el campo conectado a true
		#equivale a hacer un update de sql
		jugadoraux=Jugador.objects.get(id=idjugador) 
		jugadoraux.conectado=True
		jugadoraux.save()
		
		print ("==CONECTADO DESPUES="+str(jugadoraux.conectado))
		print ("==OK=")
		request.session['actual']=str(actual) # almacenar en una variable de sesión el jugador actual tipo cookie en ram
	
		usuarios=Jugador.objects.filter(conectado=True).order_by('-elo') #descendente -  ascendente no poner signo
	
		#la paginacion
		page = request.GET.get('page')
		print ("pagina="+str(page))
		paginator = Paginator(usuarios, 10) 
		if page == None:
			page=paginator.num_pages
			page=1
		try:
			usuarios=paginator.get_page(page)
		except PageNotAnInteger:
			usuarios = paginator.page(1)
		except EmptyPage:
			usuarios = paginator.page(paginator.num_pages)
	
	print("Jugadores conectados::::::::::::::::::::::::"+str(numconectados))
	numconectados=1
	quitartableros=1   #se ocultan los tableros
	room_name="publica" #la sala de chat pública del ajedrez
	return render(request, 'home.html', { 'usuarios': usuarios,'ganadas': ganadas,'perdidas':perdidas,
	'empatadas':empatadas, 'elo':elo, 'total':total, 'jugador1':jugador1,'jugador2':jugador2,'jugador3':jugador3,
	'contrincante1':contrincante1,'contrincante2':contrincante2,'contrincante3':contrincante3, 'actual':actual, 
	'quitartableros':quitartableros,'federacion':federacion,'room_name': room_name,'numconectados':numconectados})

def conectar(request):
	print ("--------Jugadores---------------")	
	print ("idjugador        Jugador   idusuario	conectado")	
	listajugadores = Jugador.objects.all().order_by('id')
	for r in listajugadores:
		r.conectado=True
		r.save()
		print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
	print ("==========>>>>>>>registros actualizados OK")	
	
	
	actual=request.user   #usuario actual
	idusuario=0
	idusuario=actual.id 
	print ("\n\n=====INICIO HOME=========================")
	print ("Usuario Actual == "+str(actual))
	print ("idusuario:::"+str(idusuario))
	print ("autenticado=="+str(request.user.is_authenticated))
	print ("is_active=="+str(request.user.is_active))
	
	contrincante1=str(User.objects.get(id=4))
	contrincante2=str(User.objects.get(id=5))
	contrincante3=str(User.objects.get(id=6))
	
	jugador1=str(User.objects.get(id=1))
	jugador2=str(User.objects.get(id=2))
	jugador3=str(User.objects.get(id=3))
	
	ganadas=0
	perdidas=0
	empatadas=0
	elo=0
	total=0
	federacion=""
	quitartableros=0
	numconectados=0
	
	#mostrar la lista de jugadores de la página principal
	usuarios = User.objects.all().order_by('id')
	print ("Usuarios")	
	for r in usuarios:
		print (str(r.id)+"     "+str(r.username))	
	print ("===============================")	
	
	print ("Jugadores")	
	print ("idjugador        Jugador   idusuario")	
	listajugadores = Jugador.objects.all().order_by('id')
	try:
		for r in listajugadores:
			print (str(r.id)+"                "+str(r.user.username)+"       "+str(r.user.id)+ "   "+str(r.conectado))	
			if r.conectado==True:
				numconectados=numconectados+1
	except:
		print("Error al leer jugadores")
		
	if actual=="AnonymousUser":
		print ("entra como usuario anónimo")
		
	if idusuario!=None: 
		print ("==entra cuando SI existe ="+str(idusuario))
		try:
			jugador=Jugador.objects.get(user=idusuario) #usuario current por defecto si no existe uno concreto
		except:
			#en caso de que de error que coja un usuario por defecto
			jugador=Jugador.objects.get(user=1) #usuario current por defecto si no existe uno concreto
		
		idjugador=jugador.id
		ganadas=jugador.ganadas
		perdidas=jugador.perdidas
		empatadas=jugador.empatadas
		elo=jugador.elo
		federacion=jugador.federacion
		total=ganadas+perdidas+empatadas
		
		print ("\ntotales partidas del jugador:::::"+str(total))
		print ("==federacion="+str(jugador.federacion))
		print ("==idjugador="+str(idjugador))
		print ("==CONECTADO ANTES DE ="+str(jugador.conectado))
		
		#cuando un jugador entrar en el sitio web y se loguea actualiza en la tabla el campo conectado a true
		#equivale a hacer un update de sql
		jugadoraux=Jugador.objects.get(id=idjugador) 
		jugadoraux.conectado=True
		jugadoraux.save()
		
		print ("==CONECTADO DESPUES="+str(jugadoraux.conectado))
		print ("==OK=")
		request.session['actual']=str(actual) # almacenar en una variable de sesión el jugador actual tipo cookie en ram
	
		usuarios=Jugador.objects.filter(conectado=True).order_by('-elo') #descendente -  ascendente no poner signo
	
		#la paginacion
		page = request.GET.get('page')
		print ("pagina="+str(page))
		paginator = Paginator(usuarios, 10) 
		if page == None:
			page=paginator.num_pages
			page=1
		try:
			usuarios=paginator.get_page(page)
		except PageNotAnInteger:
			usuarios = paginator.page(1)
		except EmptyPage:
			usuarios = paginator.page(paginator.num_pages)
	
	quitartableros=0   #se muestran los tableros
	room_name="publica" #la sala de chat pública del ajedrez
	return render(request, 'home.html', { 'usuarios': usuarios,'ganadas': ganadas,'perdidas':perdidas,
	'empatadas':empatadas, 'elo':elo, 'total':total, 'jugador1':jugador1,'jugador2':jugador2,'jugador3':jugador3,
	'contrincante1':contrincante1,'contrincante2':contrincante2,'contrincante3':contrincante3, 'actual':actual, 
	'quitartableros':quitartableros,'federacion':federacion,'room_name': room_name,'numconectados':numconectados})
	#return HttpResponseRedirect('http://localhost:8000')

def rechazarSolicitud(request):	
	return HttpResponse('<center><h1><b>Solicitud Rechazada!!</b></h1></center>')
 
#chat
def chat_room(request, room_id):
    room, created = Room.objects.get_or_create(id=room_id)
    reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })
  
def room(request, room_name):
	return render(request, 'home.html', {'room_name': room_name})
	
#chat	
def room(request, room_name):
    return render(request, 'home.html', {
        'room_name': room_name
    })

#################################################################3
#el generador de contenido para RSS	
#################################################################3

class AllPost(Feed):
    title = "Blog de Ajedrez"
    link = "https://chess24.com/en/"  #https://chess24.com/en
    description = "Blog de Ajedrez"

    def items(self):
        return Post.objects.order_by('-publication_date')
        
    def item_link(self, item):
        return reverse("one_post", args=[item.slug])
    
    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.content
        
    def item_pubdate(self, item):
        return item.publication_date	
		
class PostByCategory(Feed):
    def get_object(self, request, category_slug):
        return Category.objects.get(slug=category_slug)

    def title(self, obj):
        return u"chess24: Categoría %s" % obj.name

    def link(self, obj):
        return reverse("one_category", args=[obj.slug])

    def description(self, obj):
        return obj.meta_description

    def items(self, obj):
        return obj.post_set.order_by("-publication_date")
       
    def item_link(self, item):
        return reverse("one_post", args=[item.slug])
    
    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.content
        
    def item_pubdate(self, item):
        return item.publication_date	

def canalRSS(request):

	if request.GET.get("url"):
		url=request.GET["url"] 
		feed = feedparser.parse(url) #parseo del XML
	else:
		feed = None
	return render(request, "lector.html", {"feed" : feed,})

#indicamos a la vista que no verifique el token csrf con el decorador
@csrf_exempt 	
def guardar_tablero(request):
	if request.is_ajax():
		if request.POST:
			print("AJAX ENTRA POST====================")
			data = request.POST.get('fen') #table es una variable de javascript
			print("fen==============="+str(fen))
			#return HttpResponse(json.dumps(data), content_type='application/json')
			return JsonResponse(data)
		if request.GET:	
			print("AJAX ENTRA GET====================");
			fen = request.POST.get('fen') #table es una variable de javascript
			print("fen==============="+str(fen))
			#fen = request.POST['fen']
	
	
	datos = request.POST.getlist('fen')
	print("datos==================="+str(datos))
	datos_list = json.loads(datos[0])
				
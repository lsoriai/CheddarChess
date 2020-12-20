# -*- coding: utf-8 -*-

"""
ajedrez_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import unicode_literals
# los frameworks web denominan a éste archivo de mapeo url routing
from django.contrib import admin
from django.urls import path
from ajedrez_app import views
from django.conf.urls import url, include 
from ajedrez_app.views import *
# el servicio de ficheros estáticos durante el desarrollo añadiendo las líneas siguientes.
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth.views import logout #OJO la he anulado 29/8/2019
#from django.contrib.auth import logout 
from django.contrib.auth import views as auth_views 
from django.contrib.auth.decorators import login_required 
#RSS
from ajedrez_app.feeds import LatestPostsFeed

admin.autodiscover() 

urlpatterns = [
	path('admin/', admin.site.urls),
	url(r'^$', views.home,name='home'),
	url('about/', views.about,name='about'),
	url('contact/', views.contact,name='contact'),
	url('configurar/', views.configurar,name='configurar'),
	#url('jugar/', views.jugar,name='jugar'),
	#url(r'^(?P<id>\d+)/jugar$', views.jugar, name='jugar'),
	path('<int:idpartida>/<str:pcontrincante>/jugar', views.jugar, name='jugar'),
	url('jugar1/', views.jugar1,name='jugar1'),  # llama a jugar contra la máquina
	url('filtrocontrincante/', views.filtrocontrincante,name='filtrocontrincante'),
	url('contrincante/', views.contrincante,name='contrincante'),
	url('foro/', views.foro,name='foro'), 
	url('noticias/', views.noticias,name='noticias'),
	url('ranking/', views.ranking,name='ranking'),
	url('practicar/', views.practicar,name='practicar'),
	url('busqueda/', views.busqueda,name='busqueda'),
	path('ajedrez_app/', include('django.contrib.auth.urls')),
	url('iniciarjuego/', views.iniciarjuego,name='iniciarjuego'),
	url('solicitudes/', views.solicitudes,name='solicitudes'),
	url('enjuego/', views.enjuego,name='enjuego'),
	url('configuracion/', views.configuracion,name='configuracion'),

	url( r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),  #acceso al sistema
	#url(r'^logout/$',auth_views.LogoutView.as_view(template_name="useraccounts/logout.html"), name="logout"),#OJO NO HACE NADA
	url(r'^cerrar/$', views.cerrar,name='cerrar'),
	url(r'^signup/$', views.signup, name='signup'),  #aqui es el registro de usuarios
	
	#activa la confirmación del email
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
	path('stream/', views.stream, name='stream'),
	path('stockFish_init/', views.stockFish_init, name='stockFish_init'),
	
	#RSS
	url(r'^feeds/$', LatestPostsFeed(), name='feeds'), 
	url(r'^rss/main', LatestPostsFeed()), 
	url(r'^rss', LatestPostsFeed()), 
	path('canalRSS', views.canalRSS, name='canalRSS'),
	path('canalAprende', views.canalAprende, name='canalAprende'),
	
	url('desconectar/', views.desconectar,name='desconectar'),
	url('conectar/', views.conectar,name='conectar'),
	url('desconectarActual/', views.desconectarActual,name='desconectarActual'),
	url('rechazarSolicitud/', views.rechazarSolicitud,name='rechazarSolicitud'),
	path('<str:room_name>/', views.room, name='room'),
	url('guardar_tablero/', views.guardar_tablero,name='guardar_tablero'),
	
] 
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

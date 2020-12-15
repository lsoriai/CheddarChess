# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid
#para heredar del modelo de usuario
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin , BaseUserManager , User
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import re

#Modelos de la Base de datos BD_Ajedrez

COLORES_CHOICES = (
                     ('B', 'blancas'),
                     ('N', 'negras'),
                 )	
				 
ESTADO_CHOICES = (
                     ('P', 'parada'),
                     ('F', 'finalizada'),
					 ('I', 'iniciada'),
					 ('C', 'creada'), #en espera de contrincante
                 )	

RESULTADO_CHOICES = (
                     ('B', 'ganan blancas'),
                     ('N', 'ganan negras'),
					 ('E', 'empate'),
					 
                 )	

class Federacion(models.Model):  
	id = models.AutoField(primary_key=True)
	pais = models.CharField(max_length=25)
	comunidad = models.CharField(max_length=30)	
	def __str__(self):
		return '%s,%s' % (self.pais, self.comunidad)

#modelo Jugador incluye ej. 10 jugadores cada uno con su info
class Jugador(models.Model):   
	id = models.AutoField(primary_key=True)
	ganadas = models.IntegerField()   #acumulado de partidas ganadas por el jugador
	perdidas = models.IntegerField()  #acumulado de partidas perdidas por el jugador
	empatadas = models.IntegerField() #acumulado de partidas perdidas por el jugador
	elo = models.IntegerField()       #elo acumulado inicial 1800
	numfederado = models.IntegerField() # si se indica 0 es que no está federado
	conectado = models.BooleanField() #aparte de logueado en el sistema, el jugador quiere jugar
	anyosexperiencia=models.IntegerField()
	#federacion = models.OneToOneField(Federacion,on_delete=models.PROTECT) #requerido desde django 2.0
	federacion = models.ForeignKey(Federacion,null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	#user= models.OneToOneField(User,on_delete=models.PROTECT) #requerido desde django 2.0
	user= models.ForeignKey(User, null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	#user= models.ForeignKey(User, null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	#related_name='destinatario'
	esperaoponente = models.BooleanField(null=True, blank=True) 
	
class Pieza(models.Model):   
	id = models.AutoField(primary_key=True)
	nombre_pieza=models.CharField(max_length=15)
	num_pieza=models.IntegerField()
	foto=models.ImageField(upload_to='images/', null=True)
	color=models.CharField(max_length=7)
	
class Movimiento(models.Model):   
	id = models.AutoField(primary_key=True)
	num_movimiento = models.IntegerField()   #acumulado de partidas ganadas por el jugador

class Partida(models.Model):   
	id = models.AutoField(primary_key=True)
	num_partida=models.IntegerField()
	fecha_inicio = models.DateField("Fecha_Inicio",null=True,blank=True)
	duracion=models.DateTimeField()
	tiempo_establecido=models.DateTimeField()
	chat_id=models.IntegerField()
	resultado=RESULTADO_CHOICES
	estado=ESTADO_CHOICES
	jugador = models.OneToOneField(Jugador, null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0

class Tablero(models.Model):   
	id = models.AutoField(primary_key=True)
	#movimiento=models.ForeignKey(Movimiento,on_delete=models.PROTECT) #requerido desde django 2.0
	movimiento= models.OneToOneField(Movimiento,on_delete=models.PROTECT) #requerido desde django 2.0
	#partida=models.ForeignKey(Partida,on_delete=models.PROTECT) #requerido desde django 2.0
	partida= models.OneToOneField(Partida, null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	color_celda=COLORES_CHOICES
	celda=models.CharField(max_length=5)   # ejemplo 1-1  o A1  o 11  o 1.1

#este modelo se actualiza cada día con los usuarios activos, se elimina al iniciar el siguiente día
class Conectado(models.Model):  
	id = models.AutoField(primary_key=True)
	jugador=models.ForeignKey(Jugador,related_name='jugador_conectado',null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	def __str__(self):
		return '%s' % (self.jugador)

#para el canal RSS
class Posts(models.Model):
	id = models.AutoField(primary_key=True)	
	title = models.CharField(verbose_name='Titulo', null=False, max_length=50)
	body = models.CharField(verbose_name='Contenido', null=False, max_length=300)

#Las peticiones o solicitudes de partidas	
class Solicitud(models.Model):   
	id = models.AutoField(primary_key=True)
	fecha_inicio = models.DateField("Fecha_Inicio",null=True,blank=True)
	duracion=models.IntegerField()  # en segundos de la solicitud
	ahora=models.DateTimeField()
	aceptada=models.BooleanField()
	cancelada=models.BooleanField()
	jugador1 = models.ForeignKey(Jugador, related_name='solicita',null=True, blank=True,on_delete=models.PROTECT) #Realiza la petición o solicitud
	jugador2 = models.ForeignKey(Jugador, related_name='responde',null=True, blank=True,on_delete=models.PROTECT) #recibe/responde a la petición o solicitud
	partida=models.ForeignKey(Partida,related_name='partida',null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0

#para el chat	
class Chat(models.Model):   
	id = models.AutoField(primary_key=True)
	fecha = models.DateField("Fecha",null=True,blank=True)
	mensaje = models.CharField(max_length=255)	
	emisor=models.ForeignKey(Jugador,related_name='emisor',null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	destinatario=models.ForeignKey(Jugador,related_name='destinatario',null=True, blank=True,on_delete=models.PROTECT) #requerido desde django 2.0
	estado=models.IntegerField()
	def __str__(self):
		return '%s,%s,%s,%s,%s' % (self.fecha,self.mensaje,self.emisor,self.destinatario,self.estado)
	
class Room(models.Model):
    name = models.TextField()

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
	
	
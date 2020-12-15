# -*- coding: utf-8 -*-
import re
import json  #chat y operaciones de intercambio en las comunicaciones
import logging
from .models import *
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer #chat
from channels.generic.websocket import WebsocketConsumer #chat
from asgiref.sync import async_to_sync  #chat
from django.conf import settings
from .exceptions import ClientError
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
import traceback 
from django.http import HttpResponse
import channels.layers
import time
import datetime
from django.core import serializers  #para serializar el JSON

#############################################################################	
#                EL CHAT
# Es un consumidor WebSocket síncrono que acepta todas las conexiones, 
# recibe mensajes de su cliente y envía esos mensajes al mismo cliente. 
# Por ahora no transmite mensajes a otros clientes en la misma habitación.
#############################################################################

CLIENTS = []

#####################################################################################
# EL CHAT PUBLICO
#####################################################################################

class ChatConsumer(AsyncWebsocketConsumer): 
	room_group_name="home"
	channel_name="canal"
	
	async def connect(self):
		
		print("\n\n Fase 1. CONNECT . aceptando chat....")
		CLIENTS.append(self)
		
		if self.scope["user"].is_anonymous:
			# rechaza la conexión
			print("\n\n Connect anonimo queda rechazado..............")
			await self.close()
		else:
			# Aceptamos la conexión porque sino se rechaza y se desconecta
			print("\n\n Fase 1A Connect aceptando conexion...............\n")
			
			# añadir el grupo cada vez que se conecta es un broadcast
			await self.channel_layer.group_add(self.room_group_name, self.channel_name)
			await self.accept()	
			
			#cada ChatConsumer agrega su canal a un grupo cuyo nombre se basa en el nombre de la sala. 
			#Eso permitirá que ChatConsumers transmita mensajes a todos los demás ChatConsumers en la misma sala.
			
			#leemos la capa del canal
			self.channel_layer = channels.layers.get_channel_layer()
			#print("\n\n Fase 1B chaneel_layer ..............."+str(self.channel_layer))

			print(f" Fase 1B. Añadido el canal de la sala publica....  {self.channel_name} \n")
			print(f" Fase 1C. Añadida la sala publica....  {self.room_group_name} \n")
			print("\n\n Fase 1D Conexión Aceptada ...............")
			
		
	# Recibe el mensaje del WebSocket de channel
	async def receive(self, text_data=None, bytes_data=None):
	
		print("\n\n Fase 2. RECEIVE ...............")
		text_data_json = json.loads(text_data)
	
		print("\n\n Fase 2A el JSON...\n"+str(text_data_json)+" \n\n")

		mensaje=""
		nombre=""
		chat=""
		conectados=""
		
		mensaje = text_data_json['mensaje']
		nombre = text_data_json['nombre']
		
		chat=text_data_json['chat']
		#conectados=text_data_json['conectados']
		
		
		#El JSON del chat nombre+mensaje
		if chat=='si':
			print("valor de chat SI == "+str(chat))	
			mensaje = text_data_json['mensaje']
			nombre = text_data_json['nombre']
		if chat=='no':
			#El JSON del tablero jugador+fen 
			print("valor de chat NO == "+str(chat))	
		
		print("fase 2B. mensaje recibido....  "+str(mensaje))
		print("Fase 2C. socket receive nombre: ", nombre)
		print("fase 2D. chat publico....  "+str(chat))
		
		print("\n\n USUARIOS CONECTADOS AL CHAT ")
		for item in CLIENTS:
			print("Cliente: "+str(item)) #item.send(text_data)
			
		#usuarios=Jugador.objects.filter(conectado=True).order_by('-elo') 
		
		'''
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
		'''
			
		print("Fase 2D. va a enviar el JSON ")
		
		#hace una llamada al método asyncrónico home_send 
		if chat=='si':
			print("Entra en SI abajo == "+str(chat))	
			await self.channel_layer.group_send(
			'home', 
			{
				"type": "home.send",
				"nombre": nombre,
				"mensaje": mensaje,
				"chat": "si",
			})
		else:
			print("Entra en NO == "+str(chat))	
			await self.channel_layer.group_send(
			'home', 
			{
				"type": "home1.send",
				"nombre": " ",
				"mensaje": " ",
				"chat": "no",
			})
		
		print("Fase 2E. FIN DEL ENVIO: ")

	async def disconnect(self, close_code):
		print("\n\n disconnect ..............")
		CLIENTS.remove(self)
		# salir del grupo de la sala
		
	# EL método CLAVE que recibe un mensaje de grupo de una sala 
	async def home_send(self, event):
		print("mENSAJE RECIBIDO EN home_send: " + event["mensaje"])
		mensaje=event["mensaje"]
		nombre=event["nombre"]
		#envía el mensaje recibido 
		await self.send(text_data=json.dumps({
			'nombre': nombre,
			'mensaje': mensaje,
			'chat': 'si',
		}))	
		
	# EL método que recibe un mensaje de grupo de una sala 
	async def home1_send(self, event):
		print("mENSAJE RECIBIDO del table en home1_send: " + event["mensaje"])
		mensaje=event["mensaje"]
		nombre=event["nombre"]
		qusuarios=Jugador.objects.filter(conectado=True).order_by('-elo')
		serializado = serializers.serialize("json", qusuarios)
		print("serializado  "+str(serializado))
		#envía el mensaje recibido 
		await self.send(text_data=json.dumps({
			'nombre': ' ',
			'mensaje': ' ',
			'chat': 'no',
			'usuarios': serializado,
		}))		
	
#####################################################################################
# EL CHAT PRIVADO y EL TABLERO
#####################################################################################

class ChatConsumer1(AsyncWebsocketConsumer):
	room_group_name="jugar"
	channel_name="canal1"
	
	async def connect(self):
		
		print("\n\n Fase 1. CONNECT . aceptando chat privado....")
		CLIENTS.append(self)
		
		# estas logueado?
		if self.scope["user"].is_anonymous:
			# rechaza la conexión
			print("\n\n Connect anonimo queda rechazado..............")
			await self.close()
		else:
			# Aceptamos la conexión porque sino se rechaza y se desconecta
			print("\n\n Fase 1A Connect aceptando conexion privada del chat \n...............")
			
			# añadir el grupo cada vez que se conecta es un broadcast
			await self.channel_layer.group_add(self.room_group_name, self.channel_name)
			
			await self.accept()	
			
			#cada ChatConsumer agrega su canal a un grupo cuyo nombre se basa en el nombre de la sala. 
			#Eso permitirá que ChatConsumers transmita mensajes a todos los demás ChatConsumers en la misma sala.
			
			#leemos la capa del canal
			self.channel_layer = channels.layers.get_channel_layer()
			#print("\n\n Fase 1B chaneel_layer ..............."+str(self.channel_layer))

			print(f" Fase 1B. Añadido el canal de la sala privada....  {self.channel_name} \n")
			print(f" Fase 1C. Añadida la sala privada....  {self.room_group_name} \n")
			print("\n\n Fase 1D Conexión Aceptada ...............")
			
		
	# Recibe el mensaje del WebSocket de channel
	async def receive(self, text_data=None, bytes_data=None):
	
		print("\n\n Fase 2. RECEIVE ...............")
		text_data_json = json.loads(text_data)
	
		print("\n\n Fase 2A el JSON...\n"+str(text_data_json)+" \n\n")
		
		mensaje=""
		nombre=""
		jugador=""
		fen=""
		chat=text_data_json['chat']
		
		#El JSON del chat nombre+mensaje
		if chat=='si':
			#print("valor de chat SI == "+str(chat))	
			mensaje = text_data_json['mensaje']
			nombre = text_data_json['nombre']
		if chat=='no':
			#El JSON del tablero jugador+fen 
			#print("valor de chat NO == "+str(chat))	
			jugador=text_data_json['jugador']
			fen=text_data_json['fen']
				
		print("\n\n fase 2B. mensaje ...  "+str(mensaje))
		print(" Fase 2C. nombre .... ", nombre)
		print("fase 2B.  jugador ....  "+str(jugador))
		print("Fase 2C.  fen: ", fen)
		
		print("\n\n USUARIOS CONECTADOS AL CHAT ")
		for item in CLIENTS:
			print("Cliente: "+str(item))
			#item.send(text_data)
			
		print("Fase 2D. va a enviar el JSON ")
		
		#envía el mensaje recibido 
		'''
		await self.send(text_data=json.dumps({
            'mensaje': mensaje,
			'nombre': nombre,
        }))
		'''
		#hace una llamada al método asyncrónico jugar_send 
		if chat=='si':
			print("Entra en SI == "+str(chat))	
			await self.channel_layer.group_send(
			'jugar', 
			{
				"type": "jugar.send",
				"nombre": nombre,
				'mensaje': mensaje,
				'chat': 'si',
			})
		else:
			print("Entra en NO == "+str(chat))	
			await self.channel_layer.group_send(
			'jugar', 
			{
				"type": "jugar1.send",
				"jugador": jugador,
				'fen': fen,
				'chat': 'no',
			})
		
			
		print("Fase 2E. FIN DEL ENVIO: ")

	async def disconnect(self, close_code):
		print("\n\n disconnect ..............")
		CLIENTS.remove(self)
		# salir del grupo de la sala
		
	# El método CLAVE que recibe un mensaje de grupo de una sala para el chat
	async def jugar_send(self, event):
		print("mENSAJE RECIBIDO EN LA sala ptivada: " + event["mensaje"])
		mensaje=event["mensaje"]
		nombre=event["nombre"]
		# envia el mensaje del WebSocket
		await self.send(text_data=json.dumps({
			'nombre': nombre,
			'mensaje': mensaje,
			'chat':'si',
		}))	
		
	# El método CLAVE que recibe un mensaje de grupo de una sala para el tablero
	async def jugar1_send(self, event):
		print("mENSAJE RECIBIDO del tablero: " + event["jugador"])
		print("mENSAJE RECIBIDO del tablero: " + event["fen"])
		jugador=event["jugador"]
		fen=event["fen"]
		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'jugador': jugador,
			'fen': fen,
			'chat':'no',
		}))		
		

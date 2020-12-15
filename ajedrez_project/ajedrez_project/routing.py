# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import re_path #para el chat
from channels.routing import ProtocolTypeRouter,URLRouter,ChannelNameRouter  #para el chat
from channels.auth import AuthMiddlewareStack #para el chat 
from django.urls import path
from ajedrez_app import consumers
from ajedrez_app.consumers import *
import importlib
from channels.http import AsgiHandler
from django.core.exceptions import ImproperlyConfigured
from django.urls.exceptions import Resolver404
from django.urls.resolvers import URLResolver
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.sessions import SessionMiddlewareStack

#from channels.routing import route   #da problemas en la versión 2.3.1 funciona en 1.1.8
#from channels import include  da error
#from .middleware import JsonTokenAuthMiddleware

# Los enrutadores, para el enrutamiento predeterminado funcionan en el nivel de alcance y no de eventos
#la lista de mapeo para gestionar los mensajes bidirecionales de channels C/S 
#tenemos 3 tipos de canales basados en los canales por defecto asociados a funciones
# cada canal por defecto podemos crear canales propios, los consumidores que son funciones asociadas, 
#la url asociada en leyre.js

#PARA EL CHAT
application = ProtocolTypeRouter({
	#"websocket": AuthMiddlewareStack(   # WebSocket chat handler
	"websocket": AllowedHostsOriginValidator(
		AuthMiddlewareStack(
            URLRouter(
                [
					path(r'^ws/jugar/', consumers.ChatConsumer1), # sala privada
					path(r'^ws/home/',  consumers.ChatConsumer),   #sala publica
                ]
            )
        )
})


# -*- coding: utf-8 -*-

import os
import django
from channels.routing import ProtocolTypeRouter #la mas importante para asgi
from channels.routing import URLRouter
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application
from channels.auth    import AuthMiddlewareStack
from channels.http import AsgiHandler #porque django hasta la 2.2 no tiene soporte asgi
import ajedrez_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ajedrez_project.settings")
django.setup()  #antes anulada hasta 15/11/2020
application = get_default_application() #antes anulada hasta 15/11/2020

#para django superior a 2.2
'''
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            ajedrez_app.routing.websocket_urlpatterns
        )
    ),
})
'''

#para django 2.1.2
application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
})
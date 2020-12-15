# -*- coding: utf-8 -*-
# Register your models here.
from django.contrib import admin
from ajedrez_app.models import *
from django.contrib.auth.models import User  #nueva

#admin.site.register(Federacion)

class FederacionAdmin(admin.ModelAdmin):
	#list_display = [f.name for f in Federacion._meta.get_fields()]
	list_display = ('id','pais','comunidad')
	search_fields = ('pais','comunidad')
	list_filter = ('pais','comunidad')
admin.site.register(Federacion, FederacionAdmin)
 
class JugadorAdmin(admin.ModelAdmin):
	list_display = [z.name for z in Jugador._meta.get_fields()]
	#search_fields = ('numfederado','anyosexperiencia')
admin.site.register(Jugador, JugadorAdmin)

class PiezaAdmin(admin.ModelAdmin):
	list_display = [p.name for p in Pieza._meta.get_fields()]
	search_fields = ('nombre_pieza','num_pieza')
admin.site.register(Pieza, PiezaAdmin)

class MovimientoAdmin(admin.ModelAdmin):
	list_display = [m.name for m in Movimiento._meta.get_fields()]
	search_fields = ('num_movimiento',)
admin.site.register(Movimiento, MovimientoAdmin)

class PartidaAdmin(admin.ModelAdmin):
	list_display = [pa.name for pa in Partida._meta.get_fields()]
	search_fields = ('num_partida','fecha_inicio')
admin.site.register(Partida, PartidaAdmin)

class TableroAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Tablero._meta.get_fields()]
	search_fields = ('partida','movimiento')
admin.site.register(Tablero, TableroAdmin)

class ConectadoAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Conectado._meta.get_fields()]
	search_fields = ('id','jugador')
admin.site.register(Conectado, ConectadoAdmin)

class PostsAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Posts._meta.get_fields()]
	search_fields = ('id','title','body')
admin.site.register(Posts, PostsAdmin)

class SolicitudAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Solicitud._meta.get_fields()]
	search_fields = ('id','fecha_inicio','duracion','ahora','aceptada','cancelada','jugador1','jugador2','partida')
admin.site.register(Solicitud, SolicitudAdmin)

class ChatAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Chat._meta.get_fields()]
	search_fields = ('id','fecha','mensaje','emisor','destinatario','estado')
admin.site.register(Chat, ChatAdmin)

class RoomAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Room._meta.get_fields()]
	#search_fields = ('name')
admin.site.register(Room, RoomAdmin)

class MessageAdmin(admin.ModelAdmin):
	list_display = [t.name for t in Message._meta.get_fields()]
	search_fields = ('room','message','timestamp')
admin.site.register(Message, MessageAdmin)

	



# -*- coding: utf-8 -*-
#encoding:utf-8

from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.urls import reverse
from ajedrez_app.models import Posts

class LatestPostsFeed(Feed):
	title = "Noticias de CheddarChess"
	#link = "/feeds/"
	link = "http://localhost:8000"
	description = "Listado de Noticias de CheddarChess."
	#description_template = "feeds/articles.html"

	def items(self):
		print("ENTRA RSS items ")
		return Posts.objects.order_by('-id')[:10]

	def item_title(self, item):
		print("ENTRA RSS title "+str(item))
		return item.title

	def item_description(self, item):
		print("ENTRA RSS description "+str(item))
		return item.body

	def item_link(self, item):
		print("ENTRA RSS "+str(item))
		#return reverse('post_detail', args=[item.pk])
		#return "http://localhost:8000/%s"% item.slug
		return "http://localhost:8000/rss/main"
	   
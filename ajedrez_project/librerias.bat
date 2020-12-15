rem stack del proyecto
rem para real-time (chat)
rem Tornado/NGINX/APACHE/SOLR/PYSPARK-CLOUDERA Servidor WEB escalable escrito en python incluye momoko conector de postgresql
rem REDIS/ELASTIC SEARCH   Motor de base de datos  para memoria en cache estilo memcache
rem TinyMCE  markdown

rem version windows (archivo por lotes .bat) en linux es un archivo ejecutable del shell  (script del shell)
@echo off
@echo Iniciando instalación
cls
pip install django
rem redirige las url de los diferentes motores de bases de datos incluidos de terceros para el servidor
pip install dj-database-url  
pip install dj-static
rem unifica django con bootstrap
pip install django-admin-bootstrapped
rem kit de herramientas para subir a producción
pip install django-toolbelt
rem servidor gunicorn
pip install gunicorn
rem para postgresql
pip install psycopg2
pip install python-dateutil
pip install python-decouple
rem librería especializada en peticiones al servidor
pip install request 
pip install simplejson
rem para gestión de ficheros estáticos en el servidor
pip install static3
pip install urllib3
pip install --upgrade django-crispy-forms
rem muy importante para nginx e gunicorn
pip install whitenoise
pip install reportlab
rem nuevas para acceso vía oAuth2 con proveedores
pip install django-oauth-toolkit     
pip install django-cors-middleware
rem nuevas para acceso vía oAuth2 con Google
pip install social-auth-app-django
pip install python-social-auth[django]
pip install defusedxml
rem nuevas resto librerias
pip install click
pip install heroku
pip install jinja2
pip install pillow
pip install werkzeug
pip install django-scrumboard
rem nuevas para foro
rem pip install django-musette
pip install django-machina Whoosh
rem revisar si se han instalado con machina las siguientes:
pip install Django-mptt
pip install Django-haystack
pip install Markdown2
pip install Django-widget-tweaks
rem pip install django-spirit
rem motor firebird
pip install django-firebird
rem almacenar todas las librerias en el archivo de configuración
pip freeze>requirements.txt
pip install -r requirements.txt
@echo instalación Finalizada



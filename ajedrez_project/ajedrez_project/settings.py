# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import subprocess  #heroku
import dj_database_url #heroku
from django.urls import reverse_lazy #desde django 2.0
import django.contrib.auth 
from django.utils.translation import ugettext_lazy as _  
from stockfish import Stockfish #3.10.2
django.contrib.auth.LOGIN_URL = '/' 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%3fqq9n2!()vh9y+g-1+^wu@vb!6vk7lkmj18)7xf%4(d6k(ep'

# SECURITY WARNING: don't run with debug turned on in production!
#CONFIGURACION PARA MODO DESARROLLO
#DEBUG = True  #para desarrollo
#TEMPLATE_DEBUG = DEBUG  
#ALLOWED_HOSTS = ["*"] #para desarrollo
#CONFIGURACION PARA MODO PRODUCCION

'''
DEBUG = False #para producción
ALLOWED_HOSTS = ['.herokuapp.com'] #para producción
'''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  #para desarrollo 
#DEBUG = False #para producción
TEMPLATE_DEBUG = DEBUG  
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') #heroku+channels
ALLOWED_HOSTS = ["*"] #para desarrollo y producción
#ALLOWED_HOSTS = [".herokuapp.com"] #para producción 

ADMINS = (
     ('Leyre', 'leyre.soria@gmail.com'),
)
MANAGERS = ADMINS 

# Application definition
INSTALLED_APPS = [
	
	#1 Aplicaciones de Django
	'django.contrib.admin',
    'django.contrib.auth',   #habilita el sistema de autenticación de los modelos por defecto
	'django.contrib.admindocs',
    'django.contrib.contenttypes',  #permite permisos
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', #gestiona contenido estático en una sola ubicación
	'django.contrib.sites', 
	
	# 2 Aplicación para canales en tiempo real 
	'channels', # integrar los canales - channels 2.0 debe ir antes que el resto de modulos de la aplicación para que tome el control y no haya conflictos
	
	# 3 Aplicaciones y módulos del proyecto
	'ajedrez_app.apps.AjedrezAppConfig',   
	
	# 4 Aplicaciones de terceros
	'gunicorn',   
	'crispy_forms', 
	#'oauth2_provider',
	#'social_django' , #aplicación asociada a Google = social-auth-app-django  para redes sociales
	#'social.apps.django_app.default', # permite autenticar los usuarios vía redes sociales: Google, Twitter, Facebook, etc.
	#'rest_framework_social_oauth2',
	'mptt',      
	'haystack',  
	'widget_tweaks', 
]	

CRISPY_TEMPLATE_PACK = 'bootstrap4'
ROOT_URLCONF = 'ajedrez_project.urls'  #archivo que gestiona el mapeo de las url's está OK

#channels tienen que convivir con WSGI
WSGI_APPLICATION = 'ajedrez_project.wsgi.application'   #misitio.wsgi.application  está OK 

#Si da fallos en producción llevar la linea al final del archivo de configuración
#misitio.routing.application  está OK  hace que arranque ASGI/channels es el archivo routing.py
#ahora channels tomará el control de las aplicaciones instaladas con su propio servidor
ASGI_APPLICATION = "ajedrez_project.routing.application"    

#LA CAPA DEL CANAL - MECANISMO DE TRANSPORTE DE CHANNELS PARA PASAR MENSAJES DE PRODUCTORES A CONSUMIDORES
#channels, donde se envían y almacena la cola de los mensajes está OK
# OJO las capas de los canales son opcionales

#si estamos en modo desarrollo

'''
if DEBUG==True:    

	CHANNEL_LAYERS = {
		"default": {
			"BACKEND": "channels.layers.InMemoryChannelLayer",
		}
	}
'''

#si estamos en modo producción
#if DEBUG==False:  


CHANNEL_LAYERS = {
	'default': {
		'BACKEND': 'channels_redis.core.RedisChannelLayer',
		'CONFIG': {
			"hosts": [(os.environ.get('REDIS_HOST', 'localhost'),6379)],
			#"hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
			#"hosts": [config('CHANNEL_LAYERS_HOST')],    #para heroku
			#"hosts": [('127.0.0.1', 6379)],
		},
	},
}

	
CACHES = {
	"default": {
		"BACKEND": "redis_cache.RedisCache",
		"LOCATION": os.environ.get('REDIS_URL'),
		},
}


'''
    # da error:  ROUTING key found for default - this is no longer needed in Channels 2.
	CHANNEL_LAYERS = {
		"default": {
			"BACKEND": "asgi_redis.RedisChannelLayer",
			"CONFIG": {
				"hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
			},
			"ROUTING": "ajedrez_app.routing.channel_routing",  #donde se dirigen los mensajes entrantes
		},
	}

	CHANNEL_LAYERS = {
		'default': {
		'BACKEND': 'channels_redis.core.RedisChannelLayer',
			'CONFIG': {
				"hosts": [('127.0.0.1', 6379)],
		},
	},
	}
 

	CHANNEL_LAYERS = {
		'default': {
		'BACKEND': 'asgi_redis.RedisChannelLayer',   # es el brober a usar
			'CONFIG': {
				"hosts": [os.environ.get('REDIS_URL','redis://localhost:6379')],
				'capacity':100,
		},
	},
	}	
'''
	

#CHANNEL_LAYERS = {}

#Enrutamiento de canales
#channel_routing = {}


MESSAGES_TO_LOAD = 60  #la cola de mensajes de channels para el chat

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  #gestión de las sesiones mediante peticiones
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', #token de control antihacker
    'django.contrib.auth.middleware.AuthenticationMiddleware', # usa sesiones para las peticiones
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware', #heroku
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates'),], 
		#este directorio no puede estar vacío es donde busca las plantillas hay que incluirlo
		#este concretamente utiliza el directorio templates del proyecto
		#'DIRS': [os.path.join(BASE_DIR,"templates")],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [  #procesadores de contexto
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
			#Este bloque se activa cuando 'APP_DIRS': False
			#'loaders': [
            #    'django.template.loaders.filesystem.Loader',
            #    'django.template.loaders.app_directories.Loader',
            #],
        },
    },
]

WSGI_APPLICATION = 'ajedrez_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

'''
version de postgresql_psycopg2 2.7.5
'''
DATABASES = {
    'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',   
        'NAME': 'cheddarchessbd',
		'USER': 'postgres',                      
        'PASSWORD': 'admin',             
        'HOST': 'localhost',                     
        'PORT': '5432',                      
    }
}

#Stock fish configuración
{
    "Write Debug Log": "false",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1,
    "Ponder": "false",
    "Hash": 16,
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 30,
    "Minimum Thinking Time": 20,
    "Slow Mover": 80,
    "UCI_Chess960": "false",
}

AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend', 
)

WHITELISTED_DOMAINS = ['axiacore.com', 'gmail.com'] #limitación de dominios de correos que pueden entrar al sitio web
LOGIN_URL = reverse_lazy('login')  #va a la url de name='login' de urls.py por defecto /account/login
LOGIN_REDIRECT_URL  =  '/' #redirecciona en caso de que la contraseña es correcta
LOGIN_ERROR_URL = '/'
LOGOUT_REDIRECT_URL  =  '/' 
LOGOUT_URL= reverse_lazy('logout') #va a la url de name='logout' de urls.py

# register externals
EXTERNAL_LIBS_PATH = os.path.join(BASE_DIR, "_externals", "libs")
EXTERNAL_APPS_PATH = os.path.join(BASE_DIR, "_externals", "apps")
APPS_PATH = os.path.join(BASE_DIR, "apps")

# TEST PATH
TEST_ASSETS = os.path.join(BASE_DIR, "_test")

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#búsqueda de conversaciones en el foro. permite multiples motores de búsqueda
HAYSTACK_CONNECTIONS = {
    'default': {
		#'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'   # es el básico
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',   #avanzado   pip install whooos
		#'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
		#'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
		'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    },
}

# Lenguage support
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

# For django-hitcount
SESSION_SAVE_EVERY_REQUEST = True

# Internationalization  
# https://docs.djangoproject.com/en/2.0/topics/i18n/

SITE_ID = 1  
SITE_NAME = "CheddarChessOnline"
SITE_URL = "http://127.0.0.1:8000/"
LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'  
# para producción STATIC_URL = 'https://xxxx/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'static') 
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'  

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'djblets.siteconfig.context_processors.siteconfig',
    'djblets.util.context_processors.settingsVars',
    'djblets.util.context_processors.siteRoot',
    'djblets.util.context_processors.ajaxSerial',
    'djblets.util.context_processors.mediaSerial',
	'django.template.context_processors.request', 
	'social.apps.django_app.context_processors.backends', #para redes sociales
    'social.apps.django_app.context_processors.login_redirect', #para redes sociales
)

MEDIA_ROOT = ''  
MEDIA_URL = '' 

# declara la ruta donde se enlazará el contenido estático
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
	('css', os.path.join(STATIC_ROOT, 'css')),
	('js', os.path.join(STATIC_ROOT, 'js')),
	('images', os.path.join(STATIC_ROOT, 'images')),
	('img', os.path.join(STATIC_ROOT, 'img')), 
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    #os.path.join(BASE_DIR, 'ajedrez_app')
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#correo electrónico
EMAIL_USE_TLS = True 
EMAIL_USE_SSL=False
#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST='imap.gmail.com'
EMAIL_HOST_USER = 'infoclub3000@gmail.com'
EMAIL_HOST_PASSWORD = 'Adivinala'
EMAIL_PORT = 587
#SEND_BROKEN_LINK_EMAILS = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#postgresql+heroku
#db_from_env = dj_database_url.config(conn_max_age=500)   
db_from_env = dj_database_url.config()  
DATABASES['default'].update(db_from_env)

# -*- coding: utf-8 -*-
#encoding:utf-8
from __future__ import unicode_literals  #portabilidad python 2 a 3 de cadenas unicode

from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from hashlib import sha1
import random

# Create your tests here.

User= get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password= forms.CharField(widget=forms.PasswordInput)
	
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user= authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError("No existe el Usuario")
		if not user.check_password(password):
			raise forms.ValidationError("Clave incorrecta")
		if not user.is_active:
			raise forms.ValidationError("El usuario no está activo")
		return	super(UserLoginForm,self).clean(*args, **kwargs)
		
class SignupForm(forms.Form):
	#crear nueva cuenta de usuario
	#Valida que el nombre de usuario y el correo electrónico solicitados no estén en uso.
	#También requiere que la contraseña se ingrese dos veces.
	username = forms.CharField(label="Nombre de Usuario", widget=forms.TextInput())
	email = forms.EmailField(label="Correo electrónico",widget=forms.TextInput())
	password_one= forms.CharField(label="Clave", widget=forms.PasswordInput(render_value=False))
	password_two= forms.CharField(label="Confirmar Clave",widget=forms.PasswordInput(render_value=False))
	
	#Valida que el nombre de usuario sea alfanumérico y que aún no esté en uso.
	#También valida que el nombre de usuario no esté en la lista
	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			u= User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("El nombre del Usuario ya existe!!!")
		
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			u= User.objects.get(email=email)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("El email del Usuario ya existe!!!")	
		
	def clean_password(self):
		password = self.cleaned_data["password"]
		try:
			u= User.objects.get(password=password)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("El password del Usuario ya existe!!!")	
'''
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
'''
		
class RegisterForm(forms.Form):
	username = forms.CharField(label="Nombre de Usuario", widget=forms.TextInput())
	email = forms.EmailField(label="Correo electrónico",widget=forms.TextInput())
	password_one= forms.CharField(label="Clave", widget=forms.PasswordInput(render_value=False))
	password_two= forms.CharField(label="Confirmar Clave",widget=forms.PasswordInput(render_value=False))
	
	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			u= User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("El nombre del Usuario ya existe!!!")
		
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			u= User.objects.get(email=email)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("El email del Usuario ya existe!!!")

	def clean_password(self):
		password = self.cleaned_data["password"]
		try:
			u= User.objects.get(password=password)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("El password del Usuario ya existe!!!")			
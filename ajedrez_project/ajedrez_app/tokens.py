# -*- coding: utf-8 -*-
from django.contrib import admin
from ajedrez_app.models import Book, Publisher, Author
from ajedrez_app.models import Estudiante, Carrera
from ajedrez_app.models import Person

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

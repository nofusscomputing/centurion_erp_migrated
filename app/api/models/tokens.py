import hashlib
import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Field
from django.forms import ValidationError

from access.fields import *
from access.models import TenancyObject



class AuthToken(models.Model):


    def validate_note_no_token(self, note, token):
        """ Ensure plaintext token cant be saved to notes field.

        called from app.settings.views.user_settings.TokenAdd.form_valid()

        Args:
            note (Field): _Note field_
            token (Field): _Token field_

        Raises:
            ValidationError: _Validation failed_
        """

        validation: bool = True


        if str(note) == str(token):

            validation = False


        if str(token)[:9] in str(note):    # Allow user to use up to 8 chars so they can reference it.

            validation = False

        if not validation:

            raise ValidationError('Token can not be placed in the notes field.')



    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    note = models.CharField(
        blank = True,
        max_length = 50,
        default = None,
        null= True,
    )

    token = models.CharField(
        verbose_name = 'Auth Token',
        db_index=True,
        max_length = 64,
        null = False,
        blank = False,
        unique = True,
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    expires = models.DateTimeField(
        verbose_name = 'Expiry Date',
        null = False,
        blank = False
    )


    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def generate(self) -> str:

        return str(hashlib.sha256(str(self.randomword()).encode('utf-8')).hexdigest())


    def token_hash(self, token:str) -> str:

        salt = settings.SECRET_KEY

        return str(hashlib.sha256(str(token + salt).encode('utf-8')).hexdigest())


    def randomword(self) -> str:
    
        return ''.join(random.choice(string.ascii_letters) for i in range(120))


    def __str__(self):

        return self.token

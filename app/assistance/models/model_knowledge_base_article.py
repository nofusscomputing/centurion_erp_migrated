import importlib

from django.apps import apps
from django.db import models
from django.forms import ValidationError

from rest_framework.reverse import reverse

from access.fields import *
from access.models import TenancyObject

from assistance.models.knowledge_base import KnowledgeBase

def all_models() -> list(tuple()):

    models: list(tuple()) = []

    model_apps: list = [
        'access',
        'api',
        'app',
        'assistance',
        'config_management',
        'core',
        'itam',
        'itim',
        'project_management',
        'settings',
    ]

    excluded_models: list = [
        'appsettings',
        'authtoken',
        'history',
        'knowledgebase',
        'modelknowledgebasearticle',
        'notes',
        'relatedtickets',
        'ticket',
        'ticketcomment',
        'ticketlinkeditem',
        'usersettings',
    ]

    for app_model in apps.get_models():

        if(
            str(app_model._meta.app_label) in model_apps
            and str(app_model._meta.model_name) not in excluded_models
        ):

            models.append(
                (str(app_model._meta.app_label) + '.' + str(app_model._meta.model_name), str(app_model._meta.verbose_name))
            )

        models.sort(key=lambda tup: tup[1])

    return models


class ModelKnowledgeBaseArticle(TenancyObject):


    class Meta:

        default_permissions = ('add', 'delete', 'view')

        ordering = [
            'model',
            'id'
        ]

        unique_together = ('article', 'model', 'model_pk',)

        verbose_name = "Model Knowledge Base Article"

        verbose_name_plural = "Model Knowledge Base Articles"


    model_notes = None


    id = models.AutoField(
        blank=False,
        help_text = 'ID of this KB article link',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )


    article = models.ForeignKey(
        KnowledgeBase,
        blank = False,
        help_text = 'Article to be linked to model',
        null = False,
        on_delete = models.CASCADE,
        unique = False,
        verbose_name = 'Article',
    )


    model = models.CharField(
        blank = False,
        choices = all_models,
        help_text = 'Model type to link to article article',
        max_length = 50,
        null = False,
        unique = False,
        verbose_name = 'Model Type',
    )


    model_pk = models.IntegerField(
        blank = False,
        help_text = 'PK of the model the article is linked to',
        null = False,
        unique = False,
        verbose_name = 'Model Primary Key'
    )


    created = AutoCreatedField()


    modified = AutoLastModifiedField()


    page_layout: list = []

    table_fields: list = [
        'article',
        'category',
        'organization',
        'created',
        'modified',
    ]


    def clean(self):

        for model in apps.get_models():

            if(
                str(model._meta.app_label) + '.' + str(model._meta.model_name)
                ==
                self.model
            ):

                app = importlib.import_module( model.__module__ )

                model_class = getattr(app, model.__name__)

                item = model_class.objects.get(pk = self.model_pk)

                if item:

                    self.organization = item.organization


    def get_url( self, request = None ):
        """ Function not required nor-used"""

        return None

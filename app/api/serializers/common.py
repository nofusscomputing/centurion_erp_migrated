from rest_framework import serializers

from core import fields as centurion_field



class CommonModelSerializer(CommonBaseSerializer):

    model_notes = centurion_field.MarkdownField( required = False )
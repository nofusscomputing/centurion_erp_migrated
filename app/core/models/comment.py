from django.db import models

from access.models import TenancyObject



class CommentCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Comment ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    created = AutoCreatedField()

    modified = AutoCreatedField()



class Comment(
    TenancyObject,
    CommentCommonFields,
):


    class Meta:

        ordering = [
            'ticket',
            'created',
            'id',
        ]

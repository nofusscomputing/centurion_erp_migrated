from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from access.fields import *
from access.models import Team, TenancyObject



class KnowledgeBaseCategory(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Category"

        verbose_name_plural = "Categorys"


    parent_category = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Category this category belongs to',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Parent Category',
    )


    name = models.CharField(
        blank = False,
        help_text = 'Name/Title of the Category',
        max_length = 50,
        unique = False,
        verbose_name = 'Title',
    )


    slug = AutoSlugField()


    target_team = models.ManyToManyField(
        Team,
        blank = True,
        default = None,
        help_text = 'Team(s) to grant access to the article',
        verbose_name = 'Target Team(s)',
    )


    target_user = models.ForeignKey(
        User,
        blank = True,
        default = None,
        help_text = 'User(s) to grant access to the article',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Target Users(s)',
    )


    created = AutoCreatedField()


    modified = AutoLastModifiedField()


    def __str__(self):

        return self.name



class KnowledgeBase(TenancyObject):


    class Meta:

        ordering = [
            'title',
        ]

        verbose_name = "Article"

        verbose_name_plural = "Articles"


    model_notes = None


    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )


    title = models.CharField(
        blank = False,
        help_text = 'Title of the article',
        max_length = 50,
        unique = False,
        verbose_name = 'Title',
    )


    summary = models.TextField(
        blank = True,
        default = None,
        help_text = 'Short Summary of the article',
        null = True,
        verbose_name = 'Summary',
    )


    content = models.TextField(
        blank = True,
        default = None,
        help_text = 'Content of the article. Markdown is supported',
        null = True,
        verbose_name = 'Article Content',
    )


    category = models.ForeignKey(
        KnowledgeBaseCategory,
        blank = False,
        default = None,
        help_text = 'Article Category',
        max_length = 50,
        null = True,
        on_delete = models.SET_NULL,
        unique = False,
        verbose_name = 'Category',
    )


    release_date = models.DateTimeField(
        blank = True,
        default = None,
        help_text = 'Date the article will be published',
        null = True,
        verbose_name = 'Publish Date',
    )


    expiry_date = models.DateTimeField(
        blank = True,
        default = None,
        help_text = 'Date the article will be removed from published articles',
        null = True,
        verbose_name = 'End Date',
    )


    target_team = models.ManyToManyField(
        Team,
        blank = True,
        default = None,
        help_text = 'Team(s) to grant access to the article',
        verbose_name = 'Target Team(s)',
    )


    target_user = models.ForeignKey(
        User,
        blank = True,
        default = None,
        help_text = 'User(s) to grant access to the article',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Target Users(s)',
    )


    responsible_user = models.ForeignKey(
        User,
        blank = False,
        default = None,
        help_text = 'User(s) whom is considered the articles owner.',
        null = True,
        on_delete = models.SET_NULL,
        related_name = 'responsible_user',
        verbose_name = 'Responsible User',
    )


    responsible_teams = models.ManyToManyField(
        Team,
        blank = True,
        default = None,
        help_text = 'Team(s) whom is considered the articles owner.',
        related_name = 'responsible_teams',
        verbose_name = 'Responsible Team(s)',
    )


    public = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this article to be made available publically',
        verbose_name = 'Public Article',
    )


    created = AutoCreatedField()


    modified = AutoLastModifiedField()


    def __str__(self):

        return self.title

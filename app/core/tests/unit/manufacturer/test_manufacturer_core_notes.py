import pytest
import unittest
import requests

from django.test import TestCase, Client

from core.tests.abstract.notes_permissions import NotesPermissions



class ManufacturerNotes(TestCase, NotesPermissions):

    pass

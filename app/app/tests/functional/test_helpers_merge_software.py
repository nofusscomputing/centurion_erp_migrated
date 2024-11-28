from django.conf import settings as django_settings
from django.shortcuts import reverse
from django.test import TestCase, Client

from app.helpers.merge_software import merge_software


import pytest
import unittest


class MergeSoftwareHelper(TestCase):
    """ tests for function  `merge_software` """

    @classmethod
    def setUpTestData(self):
        self.data: dict = {
                'first_list': [
                    {
                        'name': 'software_1',
                        'state': 'install'
                    },
                    {
                        'name': 'software_2',
                        'state': 'install'
                    }
                ],
                'second_list': [
                    {
                        'name': 'software_1',
                        'state': 'absent'
                    },
                    {
                        'name': 'software_2',
                        'state': 'absent'
                    }
                ],
                'third_list': [
                    {
                        'name': 'software_1',
                        'state': 'other'
                    },
                    {
                        'name': 'software_2',
                        'state': 'other'
                    },
                    {
                        'name': 'software_3',
                        'state': 'install'
                    }
                ]
            }

        self.software_list_one = merge_software(self.data['first_list'], self.data['second_list'])

        self.software_list_two = merge_software(self.software_list_one, self.data['third_list'])


    def test_merging_0_0(self):
        """ ensure Second list overwrites the first app1 """

        assert self.software_list_one[0]['state'] == 'absent'


    def test_merging_0_1(self):
        """ ensure Second list overwrites the first app2 """

        assert self.software_list_one[1]['state'] == 'absent'



    def test_merging_1_0(self):
        """ ensure Second list overwrites the first app1 again """

        assert self.software_list_two[0]['state'] == 'other'


    def test_merging_1_1(self):
        """ ensure Second list overwrites the first app2 again """

        assert self.software_list_two[1]['state'] == 'other'


    def test_merging_1_new_list_item(self):
        """ ensure Second list overwrites the first app2 again """

        assert len(self.software_list_two) == 3


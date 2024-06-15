import pytest
import unittest

from django.test import TestCase



class TenancyObject(TestCase):

    # @classmethod
    # def setUpTestData(self):
    #     """ Setup Test """

    #     pass



    @pytest.mark.skip(reason="to be written")
    def test_function_save_attributes(self):
        """ Ensure save Attributes function match django default

        the save method is overridden. the function attributes must match default django method
        """
        pass
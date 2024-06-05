from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest



@pytest.mark.skip(reason="to be written")
def test_api_inventory_device_added():
    """ Device is created """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_operating_system_added():
    """ Operating System is created """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_operating_system_version_added():
    """ Operating System version is created """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_device_has_operating_system_added():
    """ Operating System version linked to device """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_device_operating_system_version_is_semver():
    """ Operating System version is full semver
    
        Operating system versions name is the major version number of semver.
        The device version is to be full semver 
     """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_no_version_cleaned():
    """ Check softare cleaned up
    
    As part of the inventory upload the software versions of software found on the device is set to null
    and before the processing is completed, the version=null software is supposed to be cleaned up.
    """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_category_added():
    """ Software category exists """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_added():
    """ Test software exists """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_category_linked_to_software():
    """ Software category linked to software """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_version_added():
    """ Test software version exists """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_version_returns_semver():
    """ Software Version from inventory returns semver if within version string """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_version_returns_original_version():
    """ Software Version from inventory returns inventoried version if no semver found """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_software_version_linked_to_software():
    """ Test software version linked to software it belongs too """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_device_has_software_version():
    """ Inventoried software is linked to device and it's the corret one"""
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_device_software_has_installed_date():
    """ Inventoried software version has install date """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_device_software_blank_installed_date_is_updated():
    """ A blank installed date of software is updated if the software was already attached to the device """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_valid_status_created():
    """ Successful inventory upload returns 201 """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_invalid_status_bad_request():
    """ Incorrectly formated inventory upload returns 400 """
    pass



@pytest.mark.skip(reason="to be written")
def test_api_inventory_exeception_status_sever_error():
    """ if the method throws an exception 500 must be returned.
    
    idea to test: add a random key to the report that is not documented
    and perform some action against it that will cause a python exception.
     """
    pass


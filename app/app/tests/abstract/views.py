import pytest
import unittest



class AddView:
    """ Testing of Display view """

    add_module: str = None
    """ Full module path to test """

    add_view: str = None
    """ View Class name to test """



class ChangeView:
    """ Testing of Display view """

    change_module: str = None
    """ Full module path to test """

    change_view: str = None
    """ Change Class name to test """



class DeleteView:
    """ Testing of Display view """

    delete_module: str = None
    """ Full module path to test """

    delete_view: str = None
    """ Delete Class name to test """



class DisplayView:
    """ Testing of Display view """

    display_module: str = None
    """ Full module path to test """

    display_view: str = None
    """ Change Class name to test """



class IndexView:
    """ Testing of Display view """

    index_module: str = None
    """ Full module path to test """

    index_view: str = None
    """ Index Class name to test """



class AllViews(
    AddView,
    ChangeView,
    DeleteView,
    DisplayView,
    IndexView
):
    """ Abstract test class containing ALL view tests """

    add_module: str = None
    """ Full module path to test """

    add_view: str = None
    """ View Class name to test """

    change_module: str = None
    """ Full module path to test """

    change_view: str = None
    """ Change Class name to test """

    delete_module: str = None
    """ Full module path to test """

    delete_view: str = None
    """ Delete Class name to test """

    display_module: str = None
    """ Full module path to test """

    display_view: str = None
    """ Change Class name to test """

    index_module: str = None
    """ Full module path to test """

    index_view: str = None
    """ Index Class name to test """


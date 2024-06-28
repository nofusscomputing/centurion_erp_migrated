import pytest
import unittest

from django.test import TestCase, Client



class APIAuthToken(TestCase):


    @pytest.mark.skip(reason="to be written")
    def test_token_create_own(self):
        """ Check correct permission for add 

        User can only create token for self.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_token_create_other_user(self):
        """ Check correct permission for add 

        User can not create token for another user.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_token_delete_own(self):
        """ Check correct permission for delete 

        User can only delete token for self.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_token_delete_other_user(self):
        """ Check correct permission for delete 

        User can not delete another users token.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_auth_invalid_token(self):
        """ Check token authentication

        Invalid token does not allow login
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_auth_success_returns_user_token(self):
        """ successful auth returns user and token object """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_auth_no_token(self):
        """ Check token authentication

        providing no token does not allow login
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_auth_expired_token(self):
        """ Check token authentication

        expired token does not allow login
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_auth_valid_token(self):
        """ Check token authentication

        Valid token allows login
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_feat_expired_token_is_removed(self):
        """ token feature confirmation

        expired token is deleted
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_token_not_saved_to_db(self):
        """ confirm generated token not saved to the database """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_header_format_invalid_token(self):
        """ token header format check
        
        header missing 'Token' prefix reports invalid
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_header_format_invalid_token_spaces(self):
        """ token header format check
        
        auth header with extra spaces reports invalid
        """
        pass

from django.test import TestCase
from django.core.mail import EmailMessage
from unittest.mock import patch
from authenticationApp.utils import send_normal_email


"""_Unit test for testing the function of sending a normal email to the user mail_
"""
class SendNormalEmailTestCase(TestCase):

    @patch('authenticationApp.utils.EmailMessage.send')
    def test_send_normal_email(self, send_mock):
        data = {
            'email_subject': 'Test Subject',
            'email_body': 'Test Body',
            'to_email': 'test@example.com',
        }

        send_normal_email(data)

        # Assert that the send method was called once
        send_mock.assert_called_once()

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from authenticationApp.models import CustomUser



class CreateModeratorTestCase(APITestCase):
    """_Unit test for testing the function of creating moderators by the admin_
    """

    def setUp(self):
        # Create a user with admin privileges for authentication
        self.admin_user = CustomUser.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Set up data for testing
        self.valid_data = {'username': 'newmoderator', 'email': 'newmoderator@example.com', 'password': 'password123'}
    def test_create_moderator(self):
        # Authenticate as admin user
        self.client.force_authenticate(user=self.admin_user)

        # Make a POST request to create a moderator
        url = reverse('create_moderator')  # Assuming the view name is 'create_moderator'
        response = self.client.post(url, data=self.valid_data)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the moderator was created in the database
        self.assertTrue(CustomUser.objects.filter(username='newmoderator').exists())

      


        


from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

client = APIClient()
factory = APIRequestFactory()

class UserTests(TestCase):
    emailLoginUrl = '/users/token/email'
    emailCreateUrl = '/users/create/email'

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail.com',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_create_user_with_invalid_email(self):
        """
        Tests that a user cannot be created with an invalid email.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)

    def test_create_user_with_invalid_password(self):
        """
        Tests that a user cannot be created with an invalid password.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail.com',
        }

        response = client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)

    def test_create_user_with_invalid_email_and_password(self):
        """
        Tests that a user cannot be created with an invalid email and password.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail',
        }

        response = client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)

    def test_user_already_exists(self):
        """
        Tests that a user cannot be created if the user already exists.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail.com',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        """
        Tests that a user can login.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail.com',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = self.emailLoginUrl
        
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access')
        self.assertContains(response, 'refresh')

    def test_user_login_with_invalid_email(self):
        """
        Tests that a user cannot login with an invalid email.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)

        url = self.emailLoginUrl

        response = client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)


    def test_user_login_with_invalid_password(self):
        """
        Tests that a user cannot login with an invalid password.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail.com',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = self.emailLoginUrl
        data = {
            'email': 'abc@gmail.com',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_invalid_email_and_password(self):
        """
        Tests that a user cannot login with an invalid email and password.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')

        url = self.emailLoginUrl
        data = {
            'email': 'abc@gmail',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_incorrect_password(self):
        """
        Tests that a user cannot login with an incorrect password.
        """
        url = self.emailCreateUrl
        data = {
            'email': 'abc@gmail.com',
            'password': 'abc123',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = self.emailLoginUrl
        data = {
            'email': 'abc@gmail.com',
            'password': 'abc1234',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
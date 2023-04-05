import json

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import User


class UserRegisterTests(APITestCase):
    url = reverse('account:register')
    data = {
        'username': 'test',
        'password': 'test1234/'
    }

    def test_valid_register(self):
        """
        Ensure we can create a new user object.
        """
        response = self.client.post(self.url, self.data)        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_password(self):
        """
        Ensure we can't create a new user object with invalid password.
        """
        data = {
            'username': 'test',
            'password': '1'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_username(self):
        """
        Ensure we can create a new user with only unique username.
        """
        self.test_valid_register()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_authenticated_with_session(self):
        """
        Ensure authenticated users with session cannot access the register page.
        """
        self.test_valid_register()
        self.client.login(username='test', password='test1234/')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_is_authenticated_with_token(self):
        """
        Ensure authenticated users with token cannot access the register page.
        """
        self.test_valid_register()
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response2 = self.client.get(self.url, self.data)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)


class UserLoginTests(APITestCase):
    url = reverse('token_obtain_pair')

    def setUp(self):
        self.username = 'test'
        self.password = 'test1234/'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        
    def test_valid_login(self):
        """
        Ensure we can login with valid data.
        """
        data = {
            'username': 'test',
            'password': 'test1234/'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in json.loads(response.content))

    def test_invalid_login(self):
        """
        Ensure we can't login with invalid data.
        """
        data = {
            'username': 'test_invalid',
            'password': 'test1234/_invalid'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_empty_data(self):
        """
        Ensure we can't login with empty data.
        """
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserUpdateTests(APITestCase):
    url1 = reverse('account:change-password')
    url2 = reverse('account:me')
    data = {
        'username': 'test',
        'password': 'test1234/'
    }

    def setUp(self):
        self.username = 'test'
        self.password = 'test1234/'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        
    def test_valid_login(self):
        """
        Ensure we can login with valid data.
        """
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def test_change_password_user_is_authenticated(self):
        """
        Ensure authenticated users cannot access the change password page.
        """
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_change_password(self):
        """
        Ensure we can change the password with valid data.
        """
        self.test_valid_login()
        data = {
            'old_password': self.data['password'],
            'new_password': 'test_new_1234/'
        }
        response = self.client.put(self.url1, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_change_password(self):
        """
        Ensure we can't change the password with invalid data.
        """
        self.test_valid_login()
        data = {
            'old_password': 'invalid_password1234/',
            'new_password': 'test_new_1234/'
        }
        response = self.client.put(self.url1, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_empty_data(self):
        """
        Ensure we can't change password with empty data.
        """
        self.test_valid_login()
        data = {
            'old_password': '',
            'new_password': ''
        }
        response = self.client.put(self.url1, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile(self):
        """
        Ensure we can update profile with some data.
        """
        self.test_valid_login()
        data = {
            "id": 1,
            "first_name": 'test_update',
            "last_name": 'test_update',
            "profile": {
                "id": 1,
                "about": 'test update profile',
                "social_account": 'test update social'
            }
        }
        response = self.client.put(self.url2, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_update_profile_with_empty_data(self):
        """
        Ensure we can update profile with empty data.
        """
        self.test_valid_login()
        data = {
            "id": 1,
            "first_name": '',
            "last_name": '',
            "profile": {
                "id": 1,
                "about": '',
                "social_account": ''
            }
        }
        response = self.client.put(self.url2, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    

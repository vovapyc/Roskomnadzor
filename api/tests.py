from rest_framework.test import APITestCase
from .models import *
from rest_framework import status
import json
from django.contrib.auth import get_user_model
User = get_user_model()


class IPAddressTests(APITestCase):
    def setUp(self):
        ProhibitedIP.objects.create(address='127.0.0.1', approved=True)

        self.user = User.objects.create_superuser(username='test', password='secret', email='test@test.com')

    def test_address_list(self):
        response = self.client.get('/api/v1/ip-addresses/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(json.loads(response.content), [{'address': '127.0.0.1'}])

    def test_non_authenticated_permissions(self):
        response = self.client.post('/api/v1/ip-addresses/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put('/api/v1/ip-addresses/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete('/api/v1/ip-addresses/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_address(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/v1/ip-addresses/', {'address': '8.8.8.8'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/v1/ip-addresses/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(json.loads(response.content), [{'address': '127.0.0.1'}, {'address': '8.8.8.8'}])


class IPRequestTests(APITestCase):
    def setUp(self):
        ProhibitedIP.objects.create(address='127.0.0.1', approved=False)

        self.user = User.objects.create_superuser(username='test', password='secret', email='test@test.com')

    def test_address_add(self):
        response = self.client.post('/api/v1/ip-requests/', {'address': '8.8.8.8'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_address(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/v1/ip-requests/1/approve/', format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        response = self.client.get('/api/v1/ip-addresses/', format='json')
        self.assertListEqual(json.loads(response.content), [{'address': '127.0.0.1'}])

    def test_refuse_address(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/ip-requests/1/refuse/', format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

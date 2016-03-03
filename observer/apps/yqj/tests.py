# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from observer.apps.base.models import Category
from observer.apps.base.tests import BaseTestCase

class APITest(BaseTestCase):

    def test_token_auth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/token-auth', self.data, format='json')
        token = response.data['token']
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        token = self.get_token()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get('/api/dashboard', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, 200)

    def test_sidebar(self):
        token = self.get_token()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get('/api/app', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, 200)
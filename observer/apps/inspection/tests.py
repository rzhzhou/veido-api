# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from observer.apps.base.tests import BaseTestCase


class APITest(BaseTestCase):

    def test_inspection_table_view(self):
        token = self.get_token()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get('/api/inspection', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, 200)

    # def test_inspection_local_view(self):
    #     token = self.get_token()
    #     csrf_client = Client(enforce_csrf_checks=True)
    #     response = csrf_client.get('/api/dashboard/local-inspection/', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
    #     self.assertEqual(response.status_code, 200)

    # def test_inspection_nation_view(self):
    #     token = self.get_token()
    #     csrf_client = Client(enforce_csrf_checks=True)
    #     response = csrf_client.get('/api/dashboard/national-inspection/', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
    #     self.assertEqual(response.status_code, 200)
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from observer.apps.base.tests import BaseTestCase


class APITest(BaseTestCase):

    def test_event_table_view(self):
        token = self.get_token()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get('/api/event', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, 200)

    def test_event_details_view(self):
        token = self.get_token()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get('/api/event/1', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, 302)
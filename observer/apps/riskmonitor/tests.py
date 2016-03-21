from django.test import Client
from django.test import TestCase
from rest_framework import status

from observer.apps.base.tests import BaseTestCase


class APITest(BaseTestCase):

    def test_home_page_view(self):
        response = self.client.get('/api/industries')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_list_view(self):
        response = self.client.get('/api/news')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_detail_view(self):
        response = self.client.get('/api/news/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

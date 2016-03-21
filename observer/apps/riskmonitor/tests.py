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

    def test_enterprises_view(self):
        response = self.client.get('/enterprises')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_view(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_filters_view(self):
        response = self.client.get('/analytics/filters')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_export_view(self):
        response = self.client.get('/analytics/export')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
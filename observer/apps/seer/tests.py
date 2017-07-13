from django.test import Client, TestCase
from rest_framework import status

from observer.apps.base.tests import BaseTestCase


class APITest(BaseTestCase):

    def test_home_page_view(self):
        response = self.client.get('/api/dashboards')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_industry_list_view(self):
        response = self.client.get('/api/industries')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_industry_detail_view(self):
        response = self.client.get('/api/industries/1')
        if response.status_code == 200:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_list_view(self):
        response = self.client.get('/api/news')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_news_detail_view(self):
        response = self.client.get('/api/news/1')
        if response.status_code == 200:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_enterprises_view(self):
        response = self.client.get('/api/enterprises')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_view(self):
        response = self.client.get('/api/analytics')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_filters_view(self):
        response = self.client.get('/api/analytics/filters')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_file_export_view(self):
        response = self.client.get('/api/analytics/export')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(response.data['url'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
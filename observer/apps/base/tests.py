# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from observer.apps.base.models import Category, Area


class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'admin@shendu.info'
        self.username = 'wuhan'
        self.password = 'wuhan'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.data = {'username':self.username, 'password': self.password}
        category = Category(name= u'质监热点')
        category.save()
        area = Area(name=u'全国', level=1)
        area.save()

    def get_token(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/token-auth', self.data, format='json')
        return response.data['token']
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group, Permission
from rest_framework.test import APIClient


class BaseTestCase():

    def get_client(self):
        email = 'admin@shendu.info'
        username = 'wuhan'
        password = 'wuhan'
        if User.objects.filter(username=username).exists() is not None:
            User.objects.create_user(username, email, password)
        udata = {'username': 'wuhan', 'password': 'wuhan'}
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/token-auth', udata)
        token = response.data['token']
        client.credentials(HTTP_AUTHORIZATION='Bearer  ' + token)
        return client

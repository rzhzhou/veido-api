import os
import sys
import django

from django.test import Client
from django.test import TestCase

from observer.apps.base.tests import BaseTestCase


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.getcwd()+'/../../../'))
def test_tools():
	reload(sys)
	sys.path.append(PROJECT_ROOT)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
	django.setup()


# test_tools()


class APITest(BaseTestCase):

    def test_home_page_view(self):
        token = self.get_token()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get('/api/dashboards', {}, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, 301)

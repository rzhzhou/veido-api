import os
import sys
import django

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(BASE_DIR+'/../../..'))

# Create your tests here.
def test_tools():
	reload(sys)
	sys.path.append(PROJECT_ROOT)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
	django.setup()
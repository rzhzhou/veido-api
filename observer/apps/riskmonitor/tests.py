import os
import sys
import django

from django.test import TestCase

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.getcwd()+'/../../../'))
def test_tools():
	reload(sys)
	sys.path.append(PROJECT_ROOT)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
	django.setup()


# test_tools()
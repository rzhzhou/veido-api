import os
import sys
import django

from django.test import TestCase

# Create your tests here.
def test_tools():
	reload(sys)
	root_mod = '/home/code/gitlab/api/'
	sys.path.append(root_mod)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
	django.setup()
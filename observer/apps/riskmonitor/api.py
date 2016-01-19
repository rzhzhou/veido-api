# -*- coding: utf-8 -*-
from tests import test_tools
test_tools()

from observer.apps.base.models import Area
print Area.objects.filter(id=3)
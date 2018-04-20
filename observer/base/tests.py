from django.test import TestCase
from rest_framework.test import APIRequestFactory

# Create your tests here.

class CorpusTestCase(TestCase):

    def __ini__(self):
        # Using the standard RequestFactory API to create a form POST request
        self.factory = APIRequestFactory()
        
    def add(self):
        request = self.factory.post('/api/corpus/add', 
            {'riskword': 'test',
            'invalidword': 'test',
            'industry_id': 'test',}
            )

    def delete(self):
         request = self.factory.delete('/api/corpus/5/')
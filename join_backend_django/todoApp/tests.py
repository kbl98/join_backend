from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import unittest
from django.http import HttpResponse
import json


# Create your tests here.
class LoginTest(TestCase):
    def test_login(self):
        self.client=Client()
        self.user=User.objects.create(username='test_user',password='test_user')
        self.client.login(username='test_user',password='test_user')
        self.client.get('/tasks/')
        response=HttpResponse()
        self.assertEqual(response.status_code, 200)

class PostTask(TestCase):
    def test_postTask(self):
        self.client = Client()
        self.user=User.objects.create(username='test_user',password='test_user')
        self.client.login(username='test_user',password='test_user')
        self.obj={'title':'testtitle','description':'testdescription','prio':'medium','category':'testcat','progress':'todo','contactNames':'[{"name":"test_user"}]','subtasks':'[]'}
       
        data=self.obj
        self.client.post('/tasks/',data)
        response=HttpResponse()
        self.assertEqual(response.status_code, 200)


        
    
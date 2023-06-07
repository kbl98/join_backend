from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import unittest
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Contact,Task
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

class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/tasks/' 
        contact_data = '[{"name": "testuser"}]'  # Als JSON-kodierte Zeichenkette
        contacts = json.loads(contact_data)
        contact=Contact.objects.create(name='testuser',email='test@mail.de',color='#ffffff',phone='098777')
        contact.save()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.obj={'color':'#ffffff','date':'testdate','title':'testtitle','description':'testdescription','prio':'medium','category':'testcat','progress':'todo','contactNames':contacts,'subtasks':'[]'}
        self.token = Token.objects.create(user=self.user)
        self.task=Task.objects.create(color='#ffffff',date='testdate',title='testtitle',description='testdescription',prio='medium',category='testcat',progress='todo')
       
        self.task.contactNames.set([contact])
        self.task.save()
        self.task_id = self.task.id 
        
        
    def test_post_request_without_token(self):
        data=self.obj
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
       

    def test_post_request_with_valid_token(self):
        data=self.obj
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str( self.token.key))
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_request_with_invalid_token(self):
        data=self.obj
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def delete_task_test(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str( self.token.key))
        task=Task.objects.get(title='testtitle')
        id = self.task_id 
        url=self.url+'/'+id+'/'
        response=self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)



        

   















        
    
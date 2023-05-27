from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Task,Letters
from .models import Contact,Subtask
from .models import users
from .serializers import TaskSerializer,ContactSerializer
from .serializers import UsernameSerializer

from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .serializers import UserSerializer

# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            newCommonUser=users.objects.create(name=request.data['username'],email=request.data['email'])
            newCommonUser.save()
            return Response({'message': 'Benutzer erfolgreich registriert.'})
        return Response(serializer.errors, status=400)

class TaskView(APIView):
    """
    View to list all tasks in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, format=None):
        """
        Return a list of all tasks.
        """
        tasks = Task.objects.all()
        print(tasks)
        serialized_tasks=TaskSerializer(instance=tasks, many=True)

        return Response(serialized_tasks.data)
    
    def post(self, request, format=None):
        data=request.data
        newTask = Task.objects.create(
            title=data['title'],description=data['description'],prio=data['prio'],date=data['date'],created_at=data['created_at'],category=data['category'],progress=data['progress'])
       
        for contact in data['contactNames']:
            print(newTask.title)
            newCont=users.objects.get(name=contact['username'])
            
            newTask.contactNames.add(newCont)

        for letter in data['letters']:
            newLett=Letters.objects.create(bothLetters=letter['bothLetters'],color=letter['color'])
            
            newTask.letters.add(newLett)

        newTask.save()
    
        serialized_Task=TaskSerializer(newTask)
        return Response(serialized_Task.data, status=status.HTTP_201_CREATED)
    
class TaskDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        oneTask = Task.objects.get(pk=pk)
        serializer = TaskSerializer(oneTask)
        return Response(serializer.data)
    
    def patch(self,request, pk,format=None):
        try:
            oneTask = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        serializer = TaskSerializer(oneTask, data=request.data,partial=True)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        print('deletestart')
        try:
            oneTask = Task.objects.filter(pk=pk)
            oneTask.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        
class loginView(ObtainAuthToken):
     def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class ContactView(APIView):
    """
    View to list all contacts in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
   

    def get(self, request, format=None):
        """
        Return a list of all contacts
        """
        contacts = Contact.objects.all()
        print(contacts)
        serialized_contacts=ContactSerializer(instance=contacts, many=True)

        return Response(serialized_contacts.data)
    
    def post(self, request, format=None):
        data=request.data
        newContact = Contact.objects.create(
            phone=data['phone'],name=data['name'],email=data['email'],color=data['color'])
       
       
    
        serialized_Contact=TaskSerializer(newContact)
        return Response(serialized_Contact.data, status=status.HTTP_201_CREATED)
    
class ContactDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        oneContact = Contact.objects.get(pk=pk)
        serializer = ContactSerializer(oneContact)
        return Response(serializer.data)
    
    def patch(self,request, pk,format=None):
        try:
            oneContact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        serializer = ContactSerializer(oneContact, data=request.data,partial=True)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        print('deletestart')
        try:
            oneContact = Contact.objects.filter(pk=pk)
            oneContact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        
class UsersView(APIView):
    """
    View to list all contacts in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all contacts
        """
        userss = users.objects.all()
        serialized_users=UsernameSerializer(instance=userss, many=True)

        return Response(serialized_users.data)
    
    def post(self, request, format=None):
        data=request.data
        newUser = users.objects.create(
            phone=data['phone'],name=data['name'],email=data['email'],color=data['color'])
       
       
    
        serialized_User=UsernameSerializer(newUser)
        return Response(serialized_User.data, status=status.HTTP_201_CREATED)
    
class UsersDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        oneUser = users.objects.get(pk=pk)
        serializer = UsernameSerializer(oneUser)
        return Response(serializer.data)
    
    def patch(self,request, pk,format=None):
        try:
            oneUser = users.objects.get(pk=pk)
        except users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        serializer = UsernameSerializer(oneUser, data=request.data,partial=True)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        print('deletestart')
        try:
            oneUser = users.objects.filter(pk=pk)
            oneUser.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        
    
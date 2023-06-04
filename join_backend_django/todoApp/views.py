from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Task
from .models import Contact,Subtask
from .models import users
from .serializers import TaskSerializer,ContactSerializer
from .serializers import UsernameSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth import authenticate


# Create your views here.
class UserRegistrationView(APIView):
    """
    Funtion to registrate a new User to the Kanbanboard by posting email, username and password 
    Test if user is already registrated.
    """
    def post(self, request):
        data=request.data
        email=data['email']
        username=data['email']
    
        if not self.username_exists(username,email):
            user=User.objects.create_user(username=data['email'],email=data['email'],password=data['password'])
            user.is_staff = True
            user.save()
            newCommonUser=users.objects.create(name=request.data['username'],email=request.data['email'],color=request.data['color'])
            newCommonUser.save()
            newContact=Contact.objects.create(name=request.data['username'],email=request.data['email'],color=request.data['color'])
            newContact.save()
            serializer=UsernameSerializer(newCommonUser)
            return JsonResponse(serializer.data)
        return JsonResponse({'Message':'User already exists'})

    def username_exists(self,username,email):
        if User.objects.filter(username=username).exists():
            return True
        if User.objects.filter(email=email).exists():
            return True
        return False   
     
class TaskView(APIView):
    """
    View to list all tasks in the system and create new task
    Requires token authentication.
    """
    authentication_classes = [authentication.TokenAuthentication]
    
    
    def get(self, request, format=None):
        """
        Returns a list of all tasks.
        """
        tasks = Task.objects.all()
        print(tasks)
        serialized_tasks=TaskSerializer(instance=tasks, many=True)
        return Response(serialized_tasks.data)
    
    def post(self, request, format=None):
        """
        Creates new Task, contactNames are user-objects, subtasks are created as objects
        """
        data=request.data
        print(data['date'])
        newTask = Task.objects.create(
            title=data['title'],description=data['description'],prio=data['prio'],date=data['date'],category=data['category'],progress=data['progress'],color=data['color'])
        print('nextStep')
        for contact in data['contactNames']:
            newCont=Contact.objects.get(name=contact['name'])
            newTask.contactNames.add(newCont)
        for subtask in data['subtasks']:
            newSubt=Subtask.objects.create(name=subtask['name'])
            newTask.subtasks.add(newSubt)
        newTask.save()
        serialized_Task=TaskSerializer(newTask)
        return Response(serialized_Task.data, status=status.HTTP_201_CREATED)
    
class TaskDetailView(APIView):
    """
    View to delete, modify or get single tasks by id
    """
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        oneTask = Task.objects.get(pk=pk)
        serializer = TaskSerializer(oneTask)
        return Response(serializer.data)
    
    def patch(self,request, pk,format=None):
        if 'subtasks'in request.data and request.data['subtasks']!=[]:
            for subtask in request.data['subtasks']:
                subtaskobj=Subtask.objects.get(id=subtask['id'])
                subtaskobj.state=subtask['state']
                subtaskobj.save()
        try:
            oneTask = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if 'contactNames' in request.data and request.data['contactNames']!=[]:
            oneTask.contactNames.clear()
            contactNames=[]
            for contact in request.data['contactNames']:
                user=Contact.objects.get(name=contact['name'])
                contactNames.append(user)
                oneTask.contactNames.set(contactNames)
        
    
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
    """
    View for login of registrated User. Returns token.
    """
    def post(self, request, *args, **kwargs):
        data=request.data
        print(data['password'])
        user = authenticate(username=data.get('email'), password=data.get('password'))
        if user is not None:
            user = User.objects.get(email=request.data['email'])
            userForColor = users.objects.get(email=request.data['email'])
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response({
                'token': token.key,
                'email': user.email,
                'id':user.id,
                'username':userForColor.name,
                'color':userForColor.color
            })
        else:
            return Response({'message':'Not User'})

class ContactView(APIView):
    """
    View to list all contacts in the system.

    Requires token authentication.

    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all contacts
        """
        contacts = Contact.objects.all()
        print(contacts)
        serialized_contacts=ContactSerializer(instance=contacts, many=True)
        return Response(serialized_contacts.data)
    
    def post(self, request, format=None):
        """
        Creates new Contact if contact doesn`t exist
        """
        data=request.data
        if not Contact.objects.filter(name=data['name']).exists():
        
            newContact = Contact.objects.create(
                phone=data['phone'],name=data['name'],email=data['email'],color=data['color'])
       
            newUser=users.objects.create(
                phone=data['phone'],name=data['name'],email=data['email'],color=data['color'])
    
            serialized_Contact=ContactSerializer(newContact)
            return Response(serialized_Contact.data, status=status.HTTP_201_CREATED)
        
    
class ContactDetailView(APIView):

    """
    Funktion to show or patch or delete a contact
    """
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
        oneContact.phone=request.data['phone']
        oneContact.email=request.data['email']
        oneContact.name=request.data['name']
        oneContact.save()
        serializer = ContactSerializer(oneContact,data=request.data,partial=True)
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
    Requires token authentication.
   
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
        try:
            oneUser = users.objects.filter(pk=pk)
            oneUser.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        
    
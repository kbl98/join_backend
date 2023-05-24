from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from django.http import Http404
from rest_framework import status

# Create your views here.
class TaskView(APIView):
    """
    View to list all tasks in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    """authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]"""

    def get(self, request, format=None):
        """
        Return a list of all tasks.
        """
        tasks = Task.objects.all()
        serialized_tasks=TaskSerializer(instance=tasks, many=True)

        return Response(serialized_tasks.data)
    
    def post(self, request, format=None):
        data=request.data
        newTask = Task.objects.create(
            title=data['title'],description=data['description'],prio=data['prio'],date=data['date'],created_at=data['created_at'],category=data['category'],progress=data['progress'],contactNames=data['contactNames'],letters=data['letters']
        )
        
        serialized_Task=TaskSerializer(newTask)
        return Response(serialized_Task, status=status.HTTP_201_CREATED)
        
    

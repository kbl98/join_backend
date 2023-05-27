"""join_backend_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todoApp.views import loginView,TaskView
from todoApp.views import TaskDetailView
from todoApp.views import ContactView,ContactDetailView
from todoApp.views import UsersView,UsersDetailView
from todoApp.views import UserRegistrationView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('contacts/', ContactView.as_view()),
    path('contacts/<int:pk>/', ContactDetailView.as_view()),
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UsersDetailView.as_view()),
    path('register/', UserRegistrationView.as_view())


]

urlpatterns = format_suffix_patterns(urlpatterns)


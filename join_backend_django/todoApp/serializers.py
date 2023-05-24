from rest_framework import serializers
from .models import Letters,Task
from .models import User,Subtask
from .models import Contact


class LettersSerializer(serializers.ModelSerializer):
   class Meta:
        model = Letters
        fields = ('bothLetters','color',)

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('username','phone','email','color',)

class TaskSerializer(serializers.ModelSerializer):
     letters=LettersSerializer(many=True)
     contactNames=UsernameSerializer(many=True)
     class Meta:
        model = Task
        fields = ('title','description','date','prio','created_at','category','progress','contactNames','letters',)


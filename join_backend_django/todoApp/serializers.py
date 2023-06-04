from rest_framework import serializers
from .models import Letters,Task
from .models import User,Subtask
from .models import Contact,users
 # If used custom user model

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)  
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username is None and password is None:
            raise serializers.ValidationError('Please provide either a username or password.')
        return attrs
    
class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = User
            fields = ['email','password']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password', 'email','id')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    
class LettersSerializer(serializers.ModelSerializer):
   class Meta:
        model = Letters
        fields = ('bothLetters','color','id')

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ('name','phone','email','color','id')

class ContactnameSerializer(serializers.ModelSerializer):
     class Meta:
        model = users
        fields = ('name')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name','phone','email','color','id')

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ('name','state','id')


class TaskSerializer(serializers.ModelSerializer):
     letters=LettersSerializer(many=True,read_only=True)
     contactNames=ContactSerializer(many=True,read_only=True)
     subtasks=SubtaskSerializer(many=True,read_only=True)
     class Meta:
        model = Task
        fields = ('id','title','description','date','prio','created_at','category','progress','contactNames','letters','subtasks','color')

     
        
           
from django.db import models
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models





# Create your models here.


PRIO_CHOICES = (
    ('urgent','urgent'),
    ('medium', 'medium'),
    ('low','low')
   
)

PROGRESS_CHOICES=(
    ('todo','todo'),
    ('in Process','in Process'),
    ('done','done'),
    ('awaiting Feedback','awaiting Feedback')
)

def return_date_time():
    now = timezone.now()
    return now + timedelta(days=7)

class users(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(blank=True,null=True , help_text='Contact email')
    phone=models.CharField(blank=True,null=True , help_text='Contact phone number',max_length=18)
    color=models.CharField(max_length=7, default="#ffffff")
    password=models.CharField(max_length=10)
    def __str__(self):
        return "{}:{}..".format(self.id, self.name)


class Letters(models.Model):
    bothLetters=models.CharField(max_length=2,blank=True,null=True )
    color = models.CharField(max_length=7, default="#ffffff")
    def __str__(self):
        return "{}:{}..".format(self.id, self.bothLetters)

class Subtask(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return "{}:{}..".format(self.id, self.title)
    


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    prio=models.CharField(max_length=6, choices=PRIO_CHOICES, default='medium')
    date=models.DateField(default=return_date_time)
    created_at = models.DateField(default=datetime.today)
    category = models.CharField(max_length=100)
    progress = models.CharField(max_length=20,choices=PROGRESS_CHOICES, default='todo')
    contactNames=models.ManyToManyField(users)
    letters=models.ManyToManyField(Letters,default='', blank=True,null=True )
    subtask=models.ForeignKey(Subtask, on_delete=models.CASCADE,blank=True,null=True)
    
class Contact(models.Model):
    name=models.CharField(max_length=100)
    phone = models.CharField(blank=True,max_length=18)
    email = models.EmailField(default="testmail@test.de")
    color = models.CharField(max_length=7, default="#ffffff")
    def __str__(self):
        return "{}:{}..".format(self.id, self.name)


 



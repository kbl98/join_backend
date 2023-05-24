from django.db import models
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from phone_field import PhoneField


# Create your models here.
from django.db import models

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

class Letters(models.Model):
    bothLetters=models.CharField(max_length=2)
    color = models.CharField(max_length=7, default="#ffffff")
    def __str__(self):
        return "{}:{}..".format(self.id, self.bothLetters)

class Subtask(models.Model):
    title = models.CharField(max_length=100)
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
    contactNames=models.ManyToManyField(User)
    letters=models.ManyToManyField(Letters,default='', blank=True,null=True )
    
class Contact(models.Model):
    name=models.CharField(max_length=100)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField
    color = models.CharField(max_length=7, default="#ffffff")
    def __str__(self):
        return "{}:{}..".format(self.id, self.paragraph[:10])


 



from django.contrib import admin
from .models import Task, Subtask
from .models import Letters

# Register your models here.
from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at')








admin.site.register(Task,TaskAdmin)
admin.site.register(Letters)



from django.contrib import admin
from .models import Contact
from .models import Task, Subtask
from .models import Letters,users

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin





class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at')








admin.site.register(users)
admin.site.register(Task,TaskAdmin)
admin.site.register(Letters)
admin.site.register(Subtask)
admin.site.register(Contact)


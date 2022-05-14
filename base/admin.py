from django.contrib import admin

from .models import Classroom, Conspect, Message, Topic, User

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Classroom)
admin.site.register(Message)
admin.site.register(Conspect)

from django.contrib import admin

from .models import User, Topic, Classroom, Message

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Classroom)
admin.site.register(Message)

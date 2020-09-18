from django.contrib import admin

# Register your models here.

from .models import Profile, Content, History, Comment

admin.site.register(Profile)
admin.site.register(Content)
admin.site.register(History)
admin.site.register(Comment)

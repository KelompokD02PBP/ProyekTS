from django.contrib import admin
from .models import ProfileUser, Like, Comment

# Register your models here.
'''
DEBUGGING PURPOSES
'''
admin.site.register(ProfileUser)
admin.site.register(Like)
admin.site.register(Comment)

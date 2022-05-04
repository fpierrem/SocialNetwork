from django.contrib import admin
from .models import User, UserProfile, Post, Comment, Follow, Like

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)

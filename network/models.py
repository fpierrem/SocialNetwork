from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass
    
class UserProfile(models.Model):    
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField()
    avatar = models.ImageField(blank=True,null=True,upload_to = "profile_pics")
    def get_avatar(self):
        return self.avatar if self.avatar else "/static/network/default_avatar.png"


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_posts')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)     

    class Meta:
        ordering = ['-timestamp']

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)     

    class Meta:
        ordering = ['-timestamp']

class Like(models.Model):
    post = models.ForeignKey(Post,null=True,on_delete=models.CASCADE, related_name='post_likes')
    comment = models.ForeignKey(Comment,null=True,on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='liked_posts')

class Follow(models.Model):
    followed = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followed_users')
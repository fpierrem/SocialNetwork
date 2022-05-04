from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass
    
class UserProfile(models.Model):    
    def validate_image(image):
        file_size = image.file.size
        limit_mb = 1
        if file_size > limit_mb * 1024 * 1024:
            raise ValidationError("Max size of file is %s MB" % limit_mb)

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField()
    avatar = models.ImageField(default="profile_pics/default_avatar.png", upload_to = "profile_pics",validators=[validate_image])


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
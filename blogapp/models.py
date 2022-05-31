
from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime





class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.CharField(blank=True,null=True,max_length=200)
    name = models.CharField(blank=True,null=True,max_length=200)
    bio = models.TextField(blank=True,null=True)
    mobile = models.CharField(blank=True,null=True,max_length=100)
    profilepic = models.ImageField(upload_to='profile_pic',default='profile_pic/user.png')
    city = models.CharField(blank=True,null=True,max_length=40)
    def __str__(self):
        return self.user.username
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(blank=True,null=True,max_length=200)
    desc = models.TextField(blank=True,null=True)
    post_img = models.ImageField(upload_to='post_img',default='profile.png')
    created_at = models.DateTimeField(default=datetime.now)
    class Meta:
        ordering = ['-created_at',]
    def __str__ (self):
        return self.title
    
class Comment(models.Model):
    post_commnet = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    
    txt = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.txt

class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    receiver = models.ForeignKey(Profile,on_delete=models.SET_NULL,related_name='msg',null=True)
    body = models.TextField()
    isread = models.BooleanField(default=False,null=True,)
    created_date = models.DateTimeField(default=datetime.now)
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    def __str__(self):
        return self.body
    class Meta:
        ordering = ['-isread','-created_date']
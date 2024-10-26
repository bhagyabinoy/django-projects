from django.db import models
from accounts.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=20,null=True, blank=True)
    slug = models.SlugField(max_length=50,null=True, blank=True)
    description = models.CharField(max_length=50,null=True, blank=True)


    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)


    # def __str__(self):
    #     return "User:  "+self.user + "|  Message : "+ self.content
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    name = models.CharField(
        max_length=64
    )
    user_pic = models.ImageField(
        upload_to='user_pics/',
        default='user_pics/default.png'
    )

    def __str__(self):
        return self.name


class ChatRoom(models.Model):
    name = models.CharField(
        max_length=64
    )
    members = models.ManyToManyField(
        to=UserProfile,
        related_name='room'
    )
    is_group = models.BooleanField(
        default=False
    )

    chat_pic = models.ImageField(
        upload_to='user_pics/',
        default='default.png'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.content

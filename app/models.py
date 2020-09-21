from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
    name = models.CharField(max_length=32)
    password = models.CharField(_('password'), max_length=128, blank=True, null=True)


class ChatRooms(models.Model):
    name = models.CharField(max_length=32, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('ChatRooms')
        verbose_name = _('ChatRooms')


class UsersInChatRooms(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    chat_room_id = models.ForeignKey(ChatRooms, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _('UsersInChatRooms')
        verbose_name = _('UsersInChatRooms')

    def __str__(self):
        return f'{self.user.username} - {self.chat_room_id.name}'


class Messages(models.Model):
    message = models.CharField(max_length=160)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    chat_room_id = models.ForeignKey(ChatRooms, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name_plural = _('Messages')
        verbose_name = _('Messages')

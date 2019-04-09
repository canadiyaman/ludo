from datetime import datetime, timedelta
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.utils import BaseModel


class Room(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=25, default='')
    is_private = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('chat:room', kwargs={"key": self.key})

    def create_roomcode(self):
        return self.roomcode_set.create(room=self)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class Participant(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_muted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ("can_ban_user", "Can Ban User"),
            ("can_mute_user", "Can Mute User"),
            ("can_delete_message", "Can Delete Message"),
            ("can_send_notification", "Can Send Notification")
        )


class Message(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return "{} - {}...".format(self.room.name, self.message[:25])

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class RoomCode(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    expire_date = models.DateTimeField(default=datetime.now() + timedelta(days=7))

    def __str__(self):
        return "{}".format(self.code)

    class Meta:
        verbose_name = 'Room Code'
        verbose_name_plural = 'Room Codes'

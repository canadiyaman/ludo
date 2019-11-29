from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

STATES = (
    ('draft', 'Taslak'),
    ('pending_chief_clerk', 'Büro Amiri Bekliyor'),
    ('pending_editor', 'Editör Bekliyor')
)
class Content(models.Model):

    state = models.CharField(choices=STATES, max_length=50)
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Content)
def content_changed(sender, created, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.state,
        {
            'type': 'chat_message',
            'message': 'New Item',
        }
    )
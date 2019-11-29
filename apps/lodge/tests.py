from channels.layers import get_channel_layer
from django.contrib.auth.models import Group, Permission

from django.test import TestCase

from apps.user.models import User


class LudgeTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='editor')
        self.user = User.objects.create(username='test_user 1', ip='100.10.1.0')
        self.user2 = User.objects.create(username='test_user 2', ip='100.10.1.1')
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.channel_layer = get_channel_layer()


    def test_channnel_layer(self):
        from asgiref.sync import async_to_sync
        message = {'type': 'hello'}
        async_to_sync(self.channel_layer.send)('test_channel', message)
        response = async_to_sync(self.channel_layer.receive)('test_channel')
        self.assertEqual(message, response)
